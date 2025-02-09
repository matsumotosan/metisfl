import random
from time import sleep
from typing import Dict, List, Union

from ..proto import model_pb2
from ..common.types import ClientParams, FederationEnvironment
from ..common.logger import MetisASCIIArt
from .controller_client import GRPCControllerClient
from .federation_monitor import FederationMonitor
from .learner_client import GRPCLearnerClient


class DriverSession(object):
    def __init__(self, fedenv: Union[str, FederationEnvironment]):
        """Initializes a new DriverSession.

        Parameters
        ----------
        fedenv : Union[str, FederationEnvironment]
            The path to the YAML file containing the federation environment or a FederationEnvironment object.
        """
        MetisASCIIArt.print()

        if isinstance(fedenv, str):
            fedenv = FederationEnvironment.from_yaml(fedenv)
        self._federation_environment = fedenv
        self._num_learners = len(self._federation_environment.learners)

        global_config = self._federation_environment.global_train_config

        self._controller_client = self._create_controller_client()
        self._learner_clients = self._create_learner_clients()
        self._service_monitor = FederationMonitor(
            controller_client=self._controller_client,
            termination_signals=self._federation_environment.termination_signals,
            is_async=global_config.communication_protocol == "Asynchronous",
        )

    def run(self) -> Dict:
        """Runs the federated training session.

        Returns
        -------
        Dict
            A dictionary containing the statistics of the federated training.
        """
        self.initialize_federation()

        statistics = self.monitor_federation()  # Blocking call.

        self.shutdown_federation()

        return statistics

    def initialize_federation(self):
        """Initialzes the federation. Picks a random Learner to obtain the intial weights from and
            ships the weights to all other Learners and the Controller.
        """

        learner_index = random.randint(0, self._num_learners - 1)

        model = self._learner_clients[learner_index].get_model(
            request_timeout=30, request_retries=2, block=True)

        self._ship_model_to_learners(model=model, skip_learner=learner_index)
        self._ship_model_to_controller(model=model)

        sleep(1)  # FIXME: Wait for the controller to receive the model.

        self.start_training()

    def start_training(self) -> None:
        """Starts the federated training."""
        # TODO: Ping controller and learners to check if they are alive.
        self._controller_client.start_training()

    def monitor_federation(self) -> Dict:
        """Monitors the federation and returns the statistics. This is a blocking call.

        Returns
        -------
        Dict
            A dictionary containing the statistics of the federated training.
        """
        return self._service_monitor.monitor_federation()  # Blocking call.

    def shutdown_federation(self):
        """Shuts down the Controller and all Learners."""

        for grpc_client in self._learner_clients:
            grpc_client.shutdown_server(request_timeout=30, block=False)
            grpc_client.shutdown()

        # FIXME:
        self._controller_client.shutdown_server(
            request_retries=2, request_timeout=30, block=True)
        self._controller_client.shutdown_client()

    def _create_controller_client(self):
        """Creates a GRPC client for the controller."""

        controller = self._federation_environment.controller

        return GRPCControllerClient(
            client_params=ClientParams(
                hostname=controller.hostname,
                port=controller.port,
                root_certificate=controller.root_certificate,
            )
        )

    def _create_learner_clients(self) -> List[GRPCLearnerClient]:
        """Creates a dictionary of GRPC clients for the learners."""

        grpc_clients: List[GRPCLearnerClient] = [None] * self._num_learners

        for idx in range(self._num_learners):

            learner = self._federation_environment.learners[idx]

            grpc_clients[idx] = GRPCLearnerClient(
                client_params=ClientParams(
                    hostname=learner.hostname,
                    port=learner.port,
                    root_certificate=learner.root_certificate,
                ),
            )

        return grpc_clients

    def _ship_model_to_controller(self, model: model_pb2.Model) -> None:
        """Encrypts and ships the model to the controller.

        Parameters
        ----------
        model : model_pb2.Model
            The Protobuf object containing the model to be shipped.
        """

        self._controller_client.set_initial_model(
            model=model,
        )

    def _ship_model_to_learners(self, model: model_pb2.Model, skip_learner: int = None) -> None:
        """Ships the given model to all Learners.

        Parameters
        ----------
        model : model_pb2.Model
            The Protobuf object containing the model to be shipped.
        skip_learner : Optional[int], (default=None)
            The index of the learner to skip.
        """

        for idx in range(self._num_learners):
            if idx == skip_learner:
                continue

            self._learner_clients[idx].set_initial_model(
                model=model,
            )

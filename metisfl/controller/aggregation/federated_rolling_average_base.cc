
#include "metisfl/controller/aggregation/federated_rolling_average_base.h"

namespace metisfl::controller {

void FederatedRollingAverageBase::InitializeModel(const Model *init_model,
                                                  double init_contrib_value) {
  wc_scaled_model = *init_model;
  score_z = init_contrib_value;

  if (!wc_scaled_model.encrypted()) {
    for (auto index = 0; index < init_model->tensors_size(); index++) {
      const auto &init_tensor = init_model->tensors(index);
      auto scaled_tensor = wc_scaled_model.mutable_tensors(index);
      auto aggregated_result = ScaleTensor(init_tensor, init_contrib_value,
                                           TensorOperation::MULTIPLY);

      *scaled_tensor->mutable_value() = aggregated_result;
    }

    // TODO(stripeli): Place logic for encrypted tensors here.
  }

  model = wc_scaled_model;
}

void FederatedRollingAverageBase::UpdateScaledModel(
    const Model *existing_model, const Model *new_model,
    double existing_contrib_value, double new_contrib_value) {
  if (!wc_scaled_model.encrypted()) {
    for (int index = 0; index < wc_scaled_model.tensors_size(); index++) {
      auto scaled_tensor = wc_scaled_model.mutable_tensors(index);

      std::string aggregated_result;

      if (existing_model->tensors_size() > 0) {
        const auto &existing_mdl_tensor = existing_model->tensors(index);
        aggregated_result =
            MergeTensors(*scaled_tensor, existing_mdl_tensor,
                         existing_contrib_value, TensorOperation::SUBTRACTION);
      }
      *scaled_tensor->mutable_value() = aggregated_result;
      aggregated_result.clear();

      auto &new_mdl_tensor = new_model->tensors(index);
      aggregated_result =
          MergeTensors(*scaled_tensor, new_mdl_tensor, new_contrib_value,
                       TensorOperation::ADDITION);

      *(scaled_tensor->mutable_value()) = aggregated_result;
    }
    // TODO(stripeli): Place logic for encrypted tensors here.
  }
}

void FederatedRollingAverageBase::UpdateCommunityModel() {
  model = Model();
  if (!wc_scaled_model.encrypted()) {
    for (const auto &scaled_mdl_variable : wc_scaled_model.tensors()) {
      auto cm_variable = model.add_tensors();
      *cm_variable = scaled_mdl_variable;
      std::string scaled_result;
      scaled_result =
          ScaleTensor(scaled_mdl_variable, score_z, TensorOperation::DIVIDE);
      *(cm_variable->mutable_value()) = scaled_result;
    }

    // TODO(stripeli): Place logic for encrypted tensors here.
  }
}

std::string FederatedRollingAverageBase::MergeTensors(
    const Tensor &tensor_spec_left, const Tensor &tensor_spec_right,
    double scaling_factor_right, TensorOperation op) {
  auto t1_l = TensorOps::DeserializeTensor(tensor_spec_left);
  auto t2_r = TensorOps::DeserializeTensor(tensor_spec_right);

  transform(t2_r.begin(), t2_r.end(), t2_r.begin(),
            std::bind(std::multiplies<double>(), std::placeholders::_1,
                      scaling_factor_right));
  if (op == TensorOperation::SUBTRACTION) {
    transform(t1_l.begin(), t1_l.end(), t2_r.begin(), t1_l.begin(),
              std::minus<double>());
  } else if (op == TensorOperation::ADDITION) {
    transform(t1_l.begin(), t1_l.end(), t2_r.begin(), t1_l.begin(),
              std::plus<double>());
  }

  auto serialized_tensor = TensorOps::SerializeTensor(t1_l);

  std::string serialized_tensor_str(serialized_tensor.begin(),
                                    serialized_tensor.end());
  return serialized_tensor_str;
}

std::string FederatedRollingAverageBase::ScaleTensor(const Tensor &tensor,
                                                     double scaling_factor,
                                                     TensorOperation op) {
  auto ts = TensorOps::DeserializeTensor(tensor);

  if (op == TensorOperation::DIVIDE) {
    transform(ts.begin(), ts.end(), ts.begin(),
              std::bind(std::divides<double>(), std::placeholders::_1,
                        scaling_factor));
  } else if (op == TensorOperation::MULTIPLY) {
    transform(ts.begin(), ts.end(), ts.begin(),
              std::bind(std::multiplies<double>(), std::placeholders::_1,
                        scaling_factor));
  }

  auto serialized_tensor = TensorOps::SerializeTensor(ts);

  std::string serialized_tensor_str(serialized_tensor.begin(),
                                    serialized_tensor.end());
  return serialized_tensor_str;
}

}  // namespace metisfl::controller

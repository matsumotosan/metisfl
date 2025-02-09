#include <pybind11/complex.h>
#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>
#include <pybind11/pytypes.h>
#include <pybind11/stl.h>

#include "metisfl/encryption/palisade/ckks_scheme.h"
#include "metisfl/encryption/palisade/encryption_scheme.h"

#define CRYPTO_CONTEXT "crypto_context"
#define CRYPTO_PUBLIC_KEY "public_key"
#define CRYPTO_PRIVATE_KEY "private_key"
#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)
namespace py = pybind11;

// We need to define CKKS as public in order
// to access its methods through PyBind.
class CKKSWrapper : public CKKS {
 public:
  ~CKKSWrapper() = default;
  CKKSWrapper(uint32_t batch_size, uint32_t scaling_factor_bits)
      : CKKS(batch_size, scaling_factor_bits) {}

  void PyGenCryptoParamsFiles(std::string crypto_context_file,
                              std::string public_key_file,
                              std::string private_key_file) {
    CryptoParamsFiles crypto_params_files{crypto_context_file, public_key_file,
                                          private_key_file};

    CKKS::GenCryptoParamsFiles(crypto_params_files);
  }

  py::dict PyGetCryptoParamsFiles() {
    py::dict py_dict_crypto_params_files;
    auto crypto_params_files = CKKS::GetCryptoParamsFiles();
    py_dict_crypto_params_files[CRYPTO_CONTEXT] =
        crypto_params_files.crypto_context_file;
    py_dict_crypto_params_files[CRYPTO_PUBLIC_KEY] =
        crypto_params_files.public_key_file;
    py_dict_crypto_params_files[CRYPTO_PRIVATE_KEY] =
        crypto_params_files.private_key_file;
    return py_dict_crypto_params_files;
  }

  py::dict PyGenCryptoParams() {
    py::dict py_dict_crypto_params;
    auto crypto_params = CKKS::GenCryptoParams();
    // Need to explicitly convert to py::str() to avoid encoding errors.
    py_dict_crypto_params[CRYPTO_CONTEXT] =
        py::str(crypto_params.crypto_context);
    py_dict_crypto_params[CRYPTO_PUBLIC_KEY] =
        py::str(crypto_params.public_key);
    py_dict_crypto_params[CRYPTO_PRIVATE_KEY] =
        py::str(crypto_params.private_key);
    return py_dict_crypto_params;
  }

  py::dict PyGetCryptoParams() {
    py::dict py_dict_crypto_params;
    auto crypto_params = CKKS::GetCryptoParams();
    // Need to explicitly convert to py::bytes() to avoid encoding errors.
    py_dict_crypto_params[CRYPTO_CONTEXT] =
        py::str(crypto_params.crypto_context);
    py_dict_crypto_params[CRYPTO_PUBLIC_KEY] =
        py::str(crypto_params.public_key);
    py_dict_crypto_params[CRYPTO_PRIVATE_KEY] =
        py::str(crypto_params.private_key);
    return py_dict_crypto_params;
  }

  py::bytes PyAggregate(py::list learners_data, py::list scaling_factors) {
    if (learners_data.size() != scaling_factors.size()) {
      PLOG(FATAL)
          << "Error: learner_data and scaling_factors size need to match";
    }

    // Simply cast the given list of data and scaling factors to
    // their corresponding std::string and std::float vectors.
    auto learners_data_vec = learners_data.cast<std::vector<std::string>>();
    auto scaling_factors_vec = scaling_factors.cast<std::vector<float>>();

    auto weighted_avg_str =
        CKKS::Aggregate(learners_data_vec, scaling_factors_vec);
    py::bytes py_bytes_avg(weighted_avg_str);
    return py_bytes_avg;
  }

  py::array_t<double> PyDecrypt(string data,
                                unsigned long int data_dimensions) {
    auto data_decrypted = CKKS::Decrypt(data, data_dimensions);
    // Cast and release created vector.
    auto py_array_decrypted =
        py::array_t<double>(py::cast(std::move(data_decrypted)));
    return py_array_decrypted;
  }

  py::bytes PyEncrypt(py::array_t<double> data_array) {
    auto data_vec = std::vector<double>(data_array.data(),
                                        data_array.data() + data_array.size());
    auto data_encrypted_str = CKKS::Encrypt(data_vec);
    py::bytes py_bytes(data_encrypted_str);
    return py_bytes;
  }
};

PYBIND11_MODULE(fhe, m) {
  m.doc() = "CKKS soft python wrapper.";
  py::class_<CKKSWrapper>(m, "CKKS")
      .def(py::init<int, int>(), py::arg("batch_size"),
           py::arg("scaling_factor_bits"))
      .def("gen_crypto_params_files", &CKKSWrapper::PyGenCryptoParamsFiles)
      .def("get_crypto_params_files", &CKKSWrapper::PyGetCryptoParamsFiles)
      .def("load_crypto_context_from_file", &CKKS::LoadCryptoContextFromFile)
      .def("load_private_key_from_file", &CKKS::LoadPrivateKeyFromFile)
      .def("load_public_key_from_file", &CKKS::LoadPublicKeyFromFile)
      .def("gen_crypto_params", &CKKSWrapper::PyGenCryptoParams)
      .def("get_crypto_params", &CKKSWrapper::PyGetCryptoParams)
      .def("load_crypto_context", &CKKS::LoadCryptoContext)
      .def("load_private_key", &CKKS::LoadPrivateKey)
      .def("load_public_key", &CKKS::LoadPublicKey)
      .def("aggregate", &CKKSWrapper::PyAggregate)
      .def("encrypt", &CKKSWrapper::PyEncrypt)
      .def(
          "decrypt",
          [](CKKSWrapper& ckks_wrapper, std::string data,
             unsigned long int data_dimensions) {
            try {
              return ckks_wrapper.PyDecrypt(data, data_dimensions);
            } catch (const py::error_already_set& e) {
              // TODO(@stripeli): We need to change the printing message
              //  when the function is invoked with wrong arguments.
              //  The following does not seem to do the trick ...
              std::string custom_msg =
                  "Error: Invalid argument types. Expected integers.";

              // Raise a new TypeError with the custom message
              PyErr_SetString(PyExc_TypeError, custom_msg.c_str());

              // Print the custom error message
              std::cerr << custom_msg << std::endl;

              // Rethrow the exception to let Python handle it
              // throw py::error_already_set();
              return py::array_t<double>();
            }
          },
          "");

  m.doc() = R"pbdoc(
        Pybind11 example plugin
        -----------------------
        .. currentmodule:: cmake_example
        .. autosummary::
           :toctree: _generate
    )pbdoc";

#ifdef VERSION_INFO
  m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
  m.attr("__version__") = "dev";
#endif
}

import React, { useState } from "react";
import { CloudUpload, CheckCircle, XCircle } from "lucide-react";


function App() {
  const [image, setImage] = useState(null);
  const [uploadStatus, setUploadStatus] = useState("");
  const [imagePreview, setImagePreview] = useState(null);
  const [response, setResponse] = useState(null);

  const API_URL = "http://localhost:8000/infer/treediculous";

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImage(file);
      setImagePreview(URL.createObjectURL(file));
      setUploadStatus("");
      setResponse(null);
    }
  };

  const handleUpload = async () => {
    if (!image) {
      setUploadStatus("Please select an image first.");
      return;
    }

    const formData = new FormData();
    formData.append("image", image);

    try {
      setUploadStatus("Uploading...");


      const response = await fetch(API_URL, {
        method: "POST",
        body: formData,
        mode: "cors",
      });

      if (!response.ok) {
        throw new Error("Upload failed");
      }

      const data = await response.json();
      setResponse(data["classname"]);
      setUploadStatus("success");
    } catch (error) {
      setUploadStatus("error");
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <div className="bg-white p-4 rounded-lg shadow-md w-full max-w-md">
        <h1 className="text-2xl font-bold mb-4 text-center text-green-600">
          Treediculous
        </h1>

        <input
          type="file"
          accept="image/*"
          onChange={handleImageChange}
          className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-green-50 file:text-green-700 hover:file:bg-green-100 mb-4"
        />

        {imagePreview && (
          <div className="mb-2 flex justify-center">
            <img
              src={imagePreview}
              alt="Preview"
              className="w-3/6 h-fit rounded-lg shadow-md"
            />
          </div>
        )}

        <button
          onClick={handleUpload}
          className="w-full py-2 px-4 bg-green-500 text-white font-semibold rounded-lg shadow-md hover:bg-green-600 focus:outline-none"
        >
          <CloudUpload className="inline-block w-5 h-5 mr-2" /> Upload
        </button>

        {uploadStatus === "Uploading..." && (
          <p className="mt-4 text-yellow-500 text-sm">Uploading your image...</p>
        )}

        {uploadStatus === "success" && (
          <p className="mt-4 text-green-500 flex items-center text-sm">
            <CheckCircle className="w-5 h-5 mr-2" /> Successfully uploaded!
          </p>
        )}

        {uploadStatus === "error" && (
          <p className="mt-4 text-red-500 flex items-center text-sm">
            <XCircle className="w-5 h-5 mr-2" /> Upload failed. Please try again.
          </p>
        )}

        {response && (
          <div className="mt-6 bg-gray-50 p-4 rounded-lg shadow">
            <h2 className="text-lg font-semibold text-gray-700">Result: {response}</h2>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
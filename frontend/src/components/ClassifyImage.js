import React, { useState } from "react";
import axios from "axios";
import { Button, Box, Typography, CircularProgress } from "@mui/material";

const ClassifyImage = () => {
  const [file, setFile] = useState(null);
  const [prediction, setPrediction] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setPrediction("");
    setError("");
  };

  const handleClassify = async (e) => {
    e.preventDefault();
    if (!file) {
      setError("Please select an image to classify.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    setPrediction("");
    setError("");

    try {
      const response = await axios.post(
        "http://localhost:8000/classify",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        },
      );
      setPrediction(response.data.prediction);
    } catch (error) {
      if (error.response && error.response.data.detail) {
        setError(error.response.data.detail);
      } else {
        setError("An error occurred during classification.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box component="form" onSubmit={handleClassify} sx={{ mt: 5 }}>
      <Typography variant="h6">Classify New Image</Typography>
      <Button variant="contained" component="label" sx={{ mt: 2 }}>
        Select Image
        <input
          type="file"
          hidden
          accept="image/*"
          onChange={handleFileChange}
        />
      </Button>
      {file && (
        <Typography variant="body2" sx={{ mt: 1 }}>
          Selected File: {file.name}
        </Typography>
      )}
      <Button
        type="submit"
        variant="contained"
        color="primary"
        sx={{ mt: 2 }}
        disabled={loading}
      >
        {loading ? <CircularProgress size={24} /> : "Classify Image"}
      </Button>
      {prediction && (
        <Typography variant="h6" color="success.main" sx={{ mt: 2 }}>
          Prediction: {prediction}
        </Typography>
      )}
      {error && (
        <Typography variant="body2" color="error" sx={{ mt: 2 }}>
          {error}
        </Typography>
      )}
    </Box>
  );
};

export default ClassifyImage;

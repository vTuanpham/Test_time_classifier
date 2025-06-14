import React, { useState } from "react";
import axios from "axios";
import { Button, Box, Typography, TextField, CircularProgress } from "@mui/material";

const ClassifyText = () => {
  const [text, setText] = useState("");
  const [prediction, setPrediction] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleClassify = async (e) => {
    e.preventDefault();
    if (!text.trim()) {
      setError("Please enter text to classify.");
      return;
    }

    const formData = new FormData();
    formData.append("text", text);

    setLoading(true);
    setPrediction("");
    setError("");

    try {
      const response = await axios.post(
        "http://localhost:8000/classify_text",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        },
      );
      setPrediction(response.data.prediction);
    } catch (err) {
      if (err.response && err.response.data.detail) {
        setError(err.response.data.detail);
      } else {
        setError("An error occurred during classification.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box component="form" onSubmit={handleClassify} sx={{ mt: 5 }}>
      <Typography variant="h6">Classify Text</Typography>
      <TextField
        label="Text"
        multiline
        fullWidth
        rows={4}
        value={text}
        onChange={(e) => setText(e.target.value)}
        sx={{ mt: 2 }}
      />
      <Button
        type="submit"
        variant="contained"
        color="primary"
        sx={{ mt: 2 }}
        disabled={loading}
      >
        {loading ? <CircularProgress size={24} /> : "Classify Text"}
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

export default ClassifyText;

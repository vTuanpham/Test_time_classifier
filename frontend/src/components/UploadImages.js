import React, { useState, useEffect } from "react";
import axios from "axios";
import {
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Button,
  Box,
  Typography,
  CircularProgress,
} from "@mui/material";

const UploadImages = () => {
  const [classes, setClasses] = useState([]);
  const [selectedClass, setSelectedClass] = useState("");
  const [files, setFiles] = useState([]);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  // Fetch existing classes on component mount
  useEffect(() => {
    const fetchClasses = async () => {
      try {
        const response = await axios.get("http://localhost:8000/classes");
        setClasses(response.data.classes);
      } catch (error) {
        setMessage("Failed to fetch classes.");
      }
    };
    fetchClasses();
  }, []);

  const handleFileChange = (e) => {
    setFiles(e.target.files);
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!selectedClass) {
      setMessage("Please select a class.");
      return;
    }
    if (files.length === 0) {
      setMessage("Please select at least one image to upload.");
      return;
    }

    const formData = new FormData();
    formData.append("class_name", selectedClass);
    for (let i = 0; i < files.length; i++) {
      formData.append("files", files[i]);
    }

    setLoading(true);
    setMessage("");

    try {
      const response = await axios.post(
        "http://localhost:8000/upload_images",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        },
      );
      setMessage(response.data.message);
      setFiles([]);
    } catch (error) {
      if (error.response && error.response.data.detail) {
        setMessage(error.response.data.detail);
      } else {
        setMessage("An error occurred while uploading images.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box component="form" onSubmit={handleUpload} sx={{ mt: 5 }}>
      <Typography variant="h6">Upload Images to Class</Typography>
      <FormControl fullWidth sx={{ mt: 2 }}>
        <InputLabel id="select-class-label">Select Class</InputLabel>
        <Select
          labelId="select-class-label"
          value={selectedClass}
          label="Select Class"
          onChange={(e) => setSelectedClass(e.target.value)}
          required
        >
          {classes.map((cls) => (
            <MenuItem key={cls} value={cls}>
              {cls}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      <Button variant="contained" component="label" sx={{ mt: 2 }}>
        Select Images
        <input
          type="file"
          hidden
          multiple
          accept="image/*"
          onChange={handleFileChange}
        />
      </Button>
      {files.length > 0 && (
        <Typography variant="body2" sx={{ mt: 1 }}>
          {files.length} file(s) selected.
        </Typography>
      )}
      <Button
        type="submit"
        variant="contained"
        color="primary"
        sx={{ mt: 2 }}
        disabled={loading}
      >
        {loading ? <CircularProgress size={24} /> : "Upload Images"}
      </Button>
      {message && (
        <Typography variant="body2" color="secondary" sx={{ mt: 2 }}>
          {message}
        </Typography>
      )}
    </Box>
  );
};

export default UploadImages;

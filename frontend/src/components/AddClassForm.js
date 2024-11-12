import React, { useState } from "react";
import axios from "axios";
import { TextField, Button, Box, Typography } from "@mui/material";

const AddClassForm = () => {
  const [className, setClassName] = useState("");
  const [message, setMessage] = useState("");

  const handleAddClass = async (e) => {
    e.preventDefault();
    if (!className.trim()) {
      setMessage("Class name cannot be empty.");
      return;
    }

    const formData = new FormData();
    formData.append("class_name", className);

    try {
      const response = await axios.post(
        "http://localhost:8000/add_class",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        },
      );
      setMessage(response.data.message);
      setClassName("");
    } catch (error) {
      if (error.response && error.response.data.detail) {
        setMessage(error.response.data.detail);
      } else {
        setMessage("An error occurred while adding the class.");
      }
    }
  };

  return (
    <Box component="form" onSubmit={handleAddClass} sx={{ mt: 3 }}>
      <Typography variant="h6">Add New Class</Typography>
      <TextField
        label="Class Name"
        variant="outlined"
        fullWidth
        value={className}
        onChange={(e) => setClassName(e.target.value)}
        required
        sx={{ mt: 2 }}
      />
      <Button type="submit" variant="contained" color="primary" sx={{ mt: 2 }}>
        Add Class
      </Button>
      {message && (
        <Typography variant="body2" color="secondary" sx={{ mt: 2 }}>
          {message}
        </Typography>
      )}
    </Box>
  );
};

export default AddClassForm;

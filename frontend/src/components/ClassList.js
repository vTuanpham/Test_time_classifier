import React, { useState, useEffect } from "react";
import axios from "axios";
import {
  Box,
  Typography,
  List,
  ListItem,
  ListItemText,
  CircularProgress,
} from "@mui/material";

const ClassList = () => {
  const [classes, setClasses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchClasses = async () => {
      try {
        const response = await axios.get("http://localhost:8000/classes");
        setClasses(response.data.classes);
      } catch (error) {
        setError("Failed to fetch classes.");
      } finally {
        setLoading(false);
      }
    };
    fetchClasses();
  }, []);

  return (
    <Box sx={{ mt: 5 }}>
      <Typography variant="h6">Available Classes</Typography>
      {loading ? (
        <CircularProgress sx={{ mt: 2 }} />
      ) : error ? (
        <Typography variant="body2" color="error" sx={{ mt: 2 }}>
          {error}
        </Typography>
      ) : classes.length === 0 ? (
        <Typography variant="body2" sx={{ mt: 2 }}>
          No classes available.
        </Typography>
      ) : (
        <List>
          {classes.map((cls) => (
            <ListItem key={cls}>
              <ListItemText primary={cls} />
            </ListItem>
          ))}
        </List>
      )}
    </Box>
  );
};

export default ClassList;

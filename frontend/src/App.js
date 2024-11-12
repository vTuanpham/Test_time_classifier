import React from "react";
import {
  Container,
  AppBar,
  Toolbar,
  Typography,
  Tabs,
  Tab,
  Box,
} from "@mui/material";
import AddClassForm from "./components/AddClassForm";
import UploadImages from "./components/UploadImages";
import ClassifyImage from "./components/ClassifyImage";
import ClassList from "./components/ClassList";

function App() {
  const [currentTab, setCurrentTab] = React.useState(0);

  const handleChange = (event, newValue) => {
    setCurrentTab(newValue);
  };

  return (
    <div>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div">
            Test-Time Compute Classifier
          </Typography>
        </Toolbar>
      </AppBar>
      <Container sx={{ mt: 4 }}>
        <Tabs value={currentTab} onChange={handleChange} centered>
          <Tab label="Add Class" />
          <Tab label="Upload Images" />
          <Tab label="Classify Image" />
          <Tab label="View Classes" />
        </Tabs>
        <TabPanel value={currentTab} index={0}>
          <AddClassForm />
        </TabPanel>
        <TabPanel value={currentTab} index={1}>
          <UploadImages />
        </TabPanel>
        <TabPanel value={currentTab} index={2}>
          <ClassifyImage />
        </TabPanel>
        <TabPanel value={currentTab} index={3}>
          <ClassList />
        </TabPanel>
      </Container>
    </div>
  );
}

// TabPanel component
function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

export default App;

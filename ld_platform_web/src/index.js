import React from "react";
import ReactDOM from "react-dom";
import { HashRouter } from "react-router-dom";
import axios from "axios";
import { ToastContainer } from "react-toastify";

// core styles
import "./scss/volt.scss";

// vendor styles
import "@fortawesome/fontawesome-free/css/all.css";
import "react-datetime/css/react-datetime.css";

import PlatformPage from "./pages/PlatformPage";
import ScrollToTop from "./components/ScrollToTop";

axios.defaults.baseURL = process.env.REACT_APP_BASE_URL;

ReactDOM.render(
  <HashRouter>
    <ScrollToTop />
    <PlatformPage />
    <ToastContainer />
  </HashRouter>,
  document.getElementById("root")
);

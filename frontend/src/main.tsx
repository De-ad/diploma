import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import { BrowserRouter, Route, Routes } from "react-router";
import { Home } from "./components/Home/Home.tsx";
import { Audit } from "./components/Audit/Audit.tsx";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="audit">
          <Route path=":websiteURL" element={<Audit />} />
        </Route>
      </Routes>
    </BrowserRouter>
  </StrictMode>,
);

import React, { useState } from "react";
import {
  getWebsiteNameFromURL,
  validateURL,
} from "../../utils/checkWebsiteURL";
import { useNavigate } from "react-router";

export const Home = () => {
  let navigate = useNavigate();
  const [websiteURL, setWebsiteURL] = useState<string>("");
  const [errorMessage, setErrorMessage] = useState<string>("");
  const [websiteImages, setWebsiteImages] = useState(null);

  const handleAudit = () => {
    if (validateURL(websiteURL)) {
      setErrorMessage("");
      let name = getWebsiteNameFromURL(websiteURL);
      navigate(`/audit/${name}`);
    } else {
      setErrorMessage("URL сайта не валидный");
    }
  };

  return (
    <div>
      <input
        placeholder="Введите URL сайта"
        onChange={(e) => setWebsiteURL(e.target.value)}
        value={websiteURL}
      ></input>
      <input type="file" id="websiteImages" name="websiteImages" accept="image/png, image/jpeg" multiple/>
      <button onClick={handleAudit}>Проанализировать</button>
      <div>{errorMessage}</div>
    </div>
  );
};

import React, { useState } from "react";
import {
  getWebsiteNameFromURL,
  validateURL,
} from "../../utils/checkWebsiteURL";
import { useNavigate } from "react-router";
import { HOME_PAGE_MESSAGE } from "../../constants/text";
import styles from "./styles.module.css";

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
    <div className={styles.block}>
      <p>{HOME_PAGE_MESSAGE}</p>
      <div className={styles.analysis_options}>
        <input
          placeholder="Введите URL сайта"
          onChange={(e) => setWebsiteURL(e.target.value)}
          value={websiteURL}
        ></input>
        <p>Анализ дизайна по визуальному представлению:</p>
        <input
          type="file"
          id="websiteImages"
          name="websiteImages"
          accept="image/png, image/jpeg"
          multiple
        />

        <p>Анализ дизайна по коду html и css:</p>
        <input
          type="file"
          id="websiteImages"
          name="websiteImages"
          accept=".html, .css"
          multiple
        />
        <button onClick={handleAudit}>Проанализировать</button>
        <div>{errorMessage}</div>
      </div>
    </div>
  );
};

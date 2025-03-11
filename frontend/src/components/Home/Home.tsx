import React, { useState } from "react";
import { validateURL } from "../../utils/checkWebsiteURL";

export const Home = () => {
  const [websiteURL, setWebsiteURL] = useState<string>("");
  const [errorMessage, setErrorMessage] = useState<string>("");

  const handleAudit = () => {
    if (validateURL(websiteURL)) {
      setErrorMessage("");
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
      <button onClick={handleAudit}>Проанализировать</button>
      <div>{errorMessage}</div>
    </div>
  );
};

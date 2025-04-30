import { useState } from "react";
import {
  getWebsiteNameFromURL,
  validateURL,
} from "../../utils/checkWebsiteURL";
import { Form } from "../Form/Form";
import { Loader } from "../Loader/Loader";
import { sendData, sendURL } from "../../api/auditApi";
import { useNavigate } from "react-router";

export const Home = () => {
  let navigate = useNavigate();
  const [errorMessage, setErrorMessage] = useState<string>("");
  const [websiteURL, setWebsiteURL] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

  const handleAudit = async () => {
    setLoading(true);
    if (validateURL(websiteURL)) {
      setErrorMessage("");
      let name = getWebsiteNameFromURL(websiteURL);
      // await sendData(websiteURL, websiteImages);
      const result = await sendURL(websiteURL);
      sessionStorage.setItem("auditResult", JSON.stringify(result));
      setLoading(false);
      navigate(`/audit/${name}`);
    } else {
      setErrorMessage("URL сайта не валидный");
    }
  };

  return (
    <>
      {loading ? (
        <Loader />
      ) : (
        <Form
          websiteURL={websiteURL}
          errorMessage={errorMessage}
          handleAudit={handleAudit}
          setWebsiteURL={setWebsiteURL}
        />
      )}
    </>
  );
};

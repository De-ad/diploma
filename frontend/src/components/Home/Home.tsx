import { useState } from "react";
import {
  getWebsiteNameFromURL,
  validateURL,
} from "../../utils/checkWebsiteURL";
import { Form } from "../Form/Form";
import { Loader } from "../Loader/Loader";
import { sendData, sendFiles, sendURL } from "../../api/auditApi";
import { useNavigate } from "react-router";
import { serializeImages } from "../../utils/convertToBase64";

export const Home = () => {
  let navigate = useNavigate();
  const [errorMessage, setErrorMessage] = useState<string>("");
  const [websiteURL, setWebsiteURL] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const [websiteImages, setWebsiteImages] = useState([]);
  const [htmlFile, setHtmlFile] = useState<File | null>(null);
  const [cssFiles, setCssFiles] = useState<File[]>([]);

  const handleAudit = async () => {
    setLoading(true);
    if (validateURL(websiteURL)) {
      setErrorMessage("");
      let name = getWebsiteNameFromURL(websiteURL);
      const vlmResult = await sendData(websiteURL, websiteImages);
      const llmResult = await sendFiles(websiteURL, htmlFile, cssFiles);
      const result = await sendURL(websiteURL);
      sessionStorage.setItem("auditResult", JSON.stringify(result));
      sessionStorage.setItem("vlmAnalyzeResult", JSON.stringify(vlmResult));
      sessionStorage.setItem("llmAnalyzeResult", JSON.stringify(llmResult));
      sessionStorage.setItem(
        "websiteImages",
        JSON.stringify(serializeImages(websiteImages)),
      );
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
          websiteImages={websiteImages}
          setWebsiteImages={setWebsiteImages}
          setHtmlFile={setHtmlFile}
          setCssFiles={setCssFiles}
        />
      )}
    </>
  );
};

import axios from "axios";
import { keysToCamel } from "../utils/caseConverter";

const axiosSEO = axios.create({
  baseURL: "http://127.0.0.1:8001",
  timeout: 30000000,
});

const axiosVLM = axios.create({
  baseURL: "http://127.0.0.1:8002",
  timeout: 30000000,
});

const applyInterceptors = (instance: any) => {
  instance.interceptors.response.use(
    (response: any) => {
      response.data = keysToCamel(response.data);
      return response;
    },
    (error: any) => {
      return Promise.reject(error);
    },
  );
};

applyInterceptors(axiosSEO);
applyInterceptors(axiosVLM);

export const sendData = async (
  websiteURL: string,
  websiteImages?: { dataURL: string }[],
) => {
  const formData = new FormData();
  formData.append("websiteURL", websiteURL);
  if (websiteImages) {
    for (let i = 0; i < websiteImages.length; i++) {
      const response = await fetch(websiteImages[i].dataURL);
      const blob = await response.blob();
      const file = new File([blob], `image_${i}`, { type: blob.type });
      formData.append("image", file);
    }
  }
  const response = await axiosVLM
    .post("/vlm/analyze", formData, {
      headers: {},
    })
    .catch(function (error) {
      console.log(error);
    });

  console.log(response.data);
  return response.data;
};

export const sendFiles = async (
  websiteURL: string,
  htmlFile: File | null,
  cssFiles: File[],
) => {
  const formData = new FormData();
  formData.append("websiteURL", websiteURL);

  if (htmlFile) {
    formData.append("htmlFile", htmlFile);
  }

  cssFiles.forEach((file, i) => {
    formData.append("cssFiles", file, `css_${i}.css`);
  });

  try {
    const response = await axiosVLM.post("/llm/analyze", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data;
  } catch (error) {
    console.error(error);
  }
};

export const sendURL = async (websiteURL: string) => {
  const response = await axiosSEO.post("/seo/analyze", {
    url: websiteURL,
  });
  console.log(response.data);
  return response.data;
};

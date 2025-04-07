import axios from "axios";

const axiosInstance = axios.create({
  baseURL: "http://127.0.0.1:8001",
  timeout: 10000,
});

export const sendData = async (websiteURL: string, websiteImages?: []) => {
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
  const response = await axiosInstance
    .post("/test", formData, {
      headers: {
        "Content-type": "multipart/form-data",
      },
    })
    .catch(function (error) {
      console.log(error);
    });

  console.log(response.data);
  return response.data;
};

import axios from "axios";

// const axiosInstance = axios.create({
//     baseURL: "https://your-api.com/api", /
//     timeout: 10000,
//     headers: {
//       "Content-Type": "application/json",
//     },
//   });

export const sendData = async (websiteURL: string, websiteImages?: []) => {
  const formData = new FormData();
  formData.append("websiteURL", websiteURL);
  console.log("he");
  if (websiteImages) {
    for (let i = 0; i < websiteImages.length; i++) {
      const response = await fetch(websiteImages[i].dataURL);
      const blob = await response.blob();
      const file = new File([blob], `image_${i}`, { type: blob.type });
      formData.append("image", file);
    }
  }
  const response = await axios
    .post("/test", formData, {
      headers: {
        "Content-type": "multipart/form-data",
      },
    })
    .then(function (response) {
      console.log(response);
    })
    .catch(function (error) {
      console.log(error);
    });
  return response.data;
};

export const convertImageToBase64 = (file: File) => {
  let reader = new FileReader();
  reader.readAsDataURL(file);
  console.log(reader.result);
};

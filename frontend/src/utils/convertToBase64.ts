export const serializeImages = (images: any[]) => {
  return images.map((img) => ({
    dataURL: img.dataURL,
    fileName: img.file?.name || "",
  }));
};

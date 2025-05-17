export const getWebsiteNameFromURL = (URL: string) => {
  URL = URL.replace(/^(https?:\/\/)?(www\.)?/, "");
  URL = URL.split("/")[0];
  return URL;
};

export const validateURL = (str: string) => {
  str = str.trimEnd();
  var pattern = new RegExp(
    "^(https?:\\/\\/)?" + // protocol
      "((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|" + // domain name
      "((\\d{1,3}\\.){3}\\d{1,3}))" + // OR ip (v4) address
      "(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*" + // port and path
      "(\\?[;&a-z\\d%_.~+=-]*)?" + // query string
      "(\\#[-a-z\\d_]*)?$",
    "i",
  );
  return !!pattern.test(str);
};

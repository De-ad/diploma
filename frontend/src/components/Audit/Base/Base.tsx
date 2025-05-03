import { SeoResult, WordCloudResult } from "../../../constants/types";
import { Cloud } from "../../Cloud/Cloud";

type Props = {
  seo: SeoResult;
  wordcloud: WordCloudResult;
};
export const Base = ({ seo, wordcloud }: Props) => {
  return (
    <>
      <p>{seo.favicon.message}</p>
      <p>{seo.robots.message}</p>
      <p>{seo.metadata.titleValue}</p>
      <p>{seo.metadata.descriptionValue}</p>
      <Cloud words={wordcloud.data} />
    </>
  );
};

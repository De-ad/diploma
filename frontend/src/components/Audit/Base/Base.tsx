import { SeoResult, WordCloudResult } from "../../../constants/types";
import { Cloud } from "../../Cloud/Cloud";
import { MdCheck, MdClose } from "react-icons/md";
import styles from "./styles.module.css";
type Props = {
  seo: SeoResult;
  wordcloud: WordCloudResult;
};
export const Base = ({ seo, wordcloud }: Props) => {
  return (
    <div className={styles.block}>
      <p>{seo.favicon.message}</p>
      <p>{seo.robots.message}</p>
      <p>{seo.metadata.titleValue}</p>
      <p>{seo.metadata.descriptionValue}</p>
      <h2>Социальные сети</h2>
      <Cloud words={wordcloud.data} />
      <h2>Search preview</h2>
      <p>
        <div className={styles.faviconAndTitle}>
          <span className={styles.favicon}>
            <div aria-hidden="true">
              {!seo.searchPreview.hasFavicon ? (
                <img
                  className={styles.image}
                  src={`${seo.searchPreview.url}/favicon.png`}
                  alt="website favicon"
                />
              ) : (
                <span className={styles.svgNoFavicon}>
                  <svg
                    focusable="false"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                    width="16px"
                    height="16px"
                  >
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"></path>
                  </svg>
                </span>
              )}
            </div>
          </span>
          <div>
            <div className={styles.googleTitle}>{seo.searchPreview.title}</div>
            <div className={styles.googleUrl}>{seo.searchPreview.url}</div>
          </div>
        </div>

        <div className={styles.googleDescription}>
          {seo.searchPreview.description}
        </div>
      </p>
    </div>
  );
};

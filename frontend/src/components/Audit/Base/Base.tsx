import {
  BrokenLink,
  KeywordsDestribution,
  PageIssues,
  PageReport,
  SeoResult,
  WordCloudResult,
} from "../../../constants/types";
import { Cloud } from "../../Cloud/Cloud";
import styles from "./styles.module.css";
import { Table } from "../../Table/Table";
import { Preview } from "./Preview/Preview";
import { Card } from "./Card";
import { SEO_PARAMS } from "../../../constants/text";

type Props = {
  seo: SeoResult;
  wordcloud: WordCloudResult;
  keywordsDistribution: KeywordsDestribution;
  pageReport: PageReport[];
};

export const Base = ({
  seo,
  wordcloud,
  keywordsDistribution,
  pageReport,
}: Props) => {
  const getCardProps = (param: (typeof SEO_PARAMS)[number]) => {
    const key = param.key as keyof PageIssues;
    let result = true;
    let description = param.description;
    let normalizedDetails: string[] | undefined;

    if (seo.seoFiles[key]) {
      result = seo.seoFiles[key].found;
    } else if (key === "socials") {
      const foundValues = Object.values(seo.socials);
      const allFound = foundValues.every(Boolean);
      const noneFound = foundValues.every((v) => !v);
      result = allFound;

      return {
        key: param.key,
        title: param.title,
        result,
        resultText: allFound
          ? param.positiveResultText
          : noneFound
            ? "Отсутствуют теги для социальных сетей"
            : param.negativeResultText,
        description: param.description,
      };
    } else {
      const collected: string[] = [];

      pageReport.forEach((page) => {
        const issueValue = page.issues[key];

        if (Array.isArray(issueValue)) {
          for (const val of issueValue) {
            collected.push(
              typeof val === "string" ? val : `${val.link} (${val.error})`,
            );
          }
        }
        if (issueValue === true) {
          collected.push(page.url);
        }
      });

      if (collected.length > 0) {
        result = false;
        normalizedDetails = [...new Set(collected)];
      }
    }

    return {
      key: param.key,
      title: param.title,
      result,
      resultText: result ? param.positiveResultText : param.negativeResultText,
      description,
      location: normalizedDetails,
    };
  };

  return (
    <div className={styles.block}>
      {SEO_PARAMS.map((param) => (
        <Card key={param.key} {...getCardProps(param)} />
      ))}
      <Preview searchPreview={seo.searchPreview} />
      <Cloud words={wordcloud.data} />
      <Table keywordsDistribution={keywordsDistribution} />
    </div>
  );
};

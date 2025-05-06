import {
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  CartesianGrid,
  Bar,
} from "recharts";
import { KeywordsDistribution } from "../../constants/types";
import styles from "./styles.module.css";

type Props = {
  keywordsDistribution: KeywordsDistribution;
};

export const Table = ({ keywordsDistribution }: Props) => {
  const allKeywords = Array.from(
    new Set([
      ...Object.keys(keywordsDistribution.title),
      ...Object.keys(keywordsDistribution.description),
      ...Object.keys(keywordsDistribution.headings),
      ...Object.keys(keywordsDistribution.total),
    ]),
  );

  const chartData = allKeywords.map((keyword) => ({
    keyword,
    total: keywordsDistribution.total[keyword] || 0,
  }));

  return (
    <div className={styles.container}>
      <h2 className={styles.heading}>
        Распределение ключевых слов по важным тегам
      </h2>
      <div className={styles.tableWrapper}>
        <table className={styles.table}>
          <thead>
            <tr>
              <th>Ключевое слово</th>
              <th>Title</th>
              <th>Description</th>
              <th>H1, H2, H3</th>
              <th>Всего</th>
            </tr>
          </thead>
          <tbody>
            {allKeywords.map((keyword, index) => (
              <tr key={keyword}>
                <td>{keyword}</td>
                <td>{keywordsDistribution.title[keyword] || "–"}</td>
                <td>{keywordsDistribution.description[keyword] || "–"}</td>
                <td>{keywordsDistribution.headings[keyword] || "–"}</td>
                <td>{keywordsDistribution.total[keyword] || "–"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className={styles.chartWrapper}>
        <h2>Распределение ключевых слов по всему содержанию</h2>
        <div
          style={{
            width: "100%",
            height: `${Math.max(300, chartData.length * 20)}px`,
          }}
        >
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData} margin={{ bottom: 60 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                dataKey="keyword"
                angle={-45}
                textAnchor="end"
                interval={0}
              />
              <YAxis />
              <Tooltip />
              <Bar dataKey="total" fill="#8c61ff" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

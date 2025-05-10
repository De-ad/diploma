import { useEffect, useState } from "react";
import { DesignAnalysis } from "../../../constants/types";
import styles from "./styles.module.css";
import { MdInfoOutline } from "react-icons/md";

export interface ImageData {
  dataURL: string;
  fileName: string;
}

export const Design = () => {
  const [websiteImages, setWebsiteImages] = useState<ImageData[] | null>(null);
  const [llmAnalyzeResult, setLlmAnalyzeResult] =
    useState<DesignAnalysis | null>(null);
  const [vlmAnalyzeResult, setVlmAnalyzeResult] =
    useState<DesignAnalysis | null>(null);

  useEffect(() => {
    let stored = sessionStorage.getItem("vlmAnalyzeResult");
    console.log(stored);
    if (stored) {
      const data = JSON.parse(stored);
      setVlmAnalyzeResult(data);
    }
    stored = sessionStorage.getItem("llmAnalyzeResult");

    if (stored) {
      const data = JSON.parse(stored);
      setLlmAnalyzeResult(data);
    }
    stored = sessionStorage.getItem("websiteImages");
    if (stored) {
      const data = JSON.parse(stored);
      setWebsiteImages(data);
    }
  }, []);

  const descriptions = [
    {
      key: "Цветовая палитра",
      value:
        "Цветовая палитра влияет на общее восприятие дизайна, создаёт настроение и помогает сформировать визуальную идентичность.",
    },
    {
      key: "Контраст",
      value:
        "Контраст влияет на читаемость и акценты, помогая выделить важные элементы и обеспечить доступность.",
    },
    {
      key: "Пробелы/отступы",
      value:
        "Пробелы и отступы влияют на визуальное дыхание макета, улучшают восприятие структуры и повышают читаемость.",
    },
    {
      key: "Макет/выравнивание по сетке",
      value:
        "Макет и выравнивание по сетке влияют на порядок и согласованность элементов, обеспечивая логичную и гармоничную структуру интерфейса.",
    },
    {
      key: "Типографика",
      value:
        "Типографика влияет на читаемость текста, его визуальную привлекательность и восприятие бренда.",
    },
    {
      key: "Визуальная иерархия",
      value:
        "Визуальная иерархия влияет на то, как пользователь воспринимает иерархию информации, помогая быстрее находить главное.",
    },
    {
      key: "Визуальная cложность",
      value:
        "Визуальная сложность влияет на уровень когнитивной нагрузки, определяя, насколько легко воспринимать и использовать интерфейс.",
    },
  ];

  const renderAnalysis = (data: DesignAnalysis) => {
    return (
      <table className={styles.table}>
        <thead>
          <tr>
            <th>Параметр</th>
            <th>Оценка (1–100)</th>
            <th>Комментарий</th>
          </tr>
        </thead>
        <tbody>
          {data.message.criteria.map((item, idx) => {
            const description = descriptions[idx];
            const tooltipText = description.value;

            return (
              <tr key={idx}>
                <td>
                  <div className={styles.paramWithTooltip}>
                    <span>{item.attribute}</span>
                    <div className={styles.tooltipIcon}>
                      <MdInfoOutline />
                      <div className={styles.tooltip}>{tooltipText}</div>
                    </div>
                  </div>
                </td>
                <td>{item.grade}</td>
                <td>{item.output}</td>
              </tr>
            );
          })}
          <tr className={styles.finalGradeRow}>
            <td colSpan={2}>
              <strong>Итоговая оценка:</strong>
            </td>
            <td>
              <strong>{data.message.finalGrade}</strong>
            </td>
          </tr>
        </tbody>
      </table>
    );
  };

  return (
    <div className={styles.container}>
      <h2>Загруженные изображения</h2>
      <div className={styles.imageGrid}>
        {websiteImages?.map((img, idx) => (
          <div key={idx} className={styles.imageCard}>
            <img src={img.dataURL} alt={`uploaded-${idx}`} />
            <p>{img.fileName}</p>
          </div>
        ))}
      </div>

      {vlmAnalyzeResult && (
        <>
          <h2>VLM анализ</h2>
          {renderAnalysis(vlmAnalyzeResult)}
        </>
      )}

      {llmAnalyzeResult && (
        <>
          <h2>LLM анализ</h2>
          {renderAnalysis(llmAnalyzeResult)}
        </>
      )}
    </div>
  );
};

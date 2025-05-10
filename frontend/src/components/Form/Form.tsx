import { useState } from "react";
import { HOME_PAGE_MESSAGE } from "../../constants/text";
import styles from "./styles.module.css";
import ImageUploading, { ImageListType } from "react-images-uploading";
import { MdClose, MdModeEdit } from "react-icons/md";

type Props = {
  setWebsiteURL: React.Dispatch<React.SetStateAction<string>>;
  websiteURL: string;
  handleAudit: () => Promise<void>;
  errorMessage: string;
  websiteImages: ImageListType;
  setWebsiteImages: React.Dispatch<React.SetStateAction<ImageListType>>;
  setHtmlFile: React.Dispatch<React.SetStateAction<File | null>>;
  setCssFiles: React.Dispatch<React.SetStateAction<File[]>>;
};

export const Form = ({
  setWebsiteURL,
  websiteURL,
  handleAudit,
  errorMessage,
  websiteImages,
  setWebsiteImages,
  setCssFiles,
  setHtmlFile,
}: Props) => {
  const maxNumber = 5;
  const [htmlFile, updateHtmlFile] = useState<File | null>(null);
  const [cssFileList, updateCssFileList] = useState<File[]>([]);

  const handleImageChange = (
    imageList: ImageListType,
    addUpdateIndex: number[] | undefined,
  ) => {
    setWebsiteImages(imageList);
  };

  return (
    <div className={styles.container}>
      <h2 className={styles.heading}>SEO-анализ сайта</h2>
      <p className={styles.subheading}>{HOME_PAGE_MESSAGE}</p>

      <label className={styles.label} htmlFor="websiteUrl">
        Введите URL сайта:
      </label>
      <input
        id="websiteUrl"
        className={styles.input}
        placeholder="https://example.com"
        onChange={(e) => setWebsiteURL(e.target.value)}
        value={websiteURL}
      />

      <div className={styles.section}>
        <p className={styles.label}>Выберите до 5 изображений:</p>
        <ImageUploading
          multiple
          value={websiteImages}
          onChange={handleImageChange}
          maxNumber={maxNumber}
        >
          {({
            imageList,
            onImageUpload,
            onImageRemoveAll,
            onImageUpdate,
            onImageRemove,
            isDragging,
            dragProps,
          }) => (
            <div className={styles.uploadArea}>
              <button
                type="button"
                className={styles.button}
                style={isDragging ? { color: "red" } : undefined}
                onClick={onImageUpload}
                {...dragProps}
              >
                Загрузить изображения
              </button>
              {websiteImages.length > 1 && (
                <button
                  type="button"
                  className={styles.removeAll}
                  onClick={onImageRemoveAll}
                >
                  Удалить все
                </button>
              )}
              <div className={styles.imagePreviewGrid}>
                {imageList.map((image, index) => (
                  <div key={index} className={styles.imageCard}>
                    <img src={image.dataURL} alt={`Preview ${index}`} />
                    <div className={styles.imageActions}>
                      <button onClick={() => onImageUpdate(index)}>
                        <MdModeEdit />
                      </button>
                      <button onClick={() => onImageRemove(index)}>
                        <MdClose />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </ImageUploading>
      </div>

      <div className={styles.fileContainer}>
        <p>Загрузите HTML файл</p>
        <input
          type="file"
          accept=".html"
          className={styles.hiddenInput}
          id="htmlUpload"
          onChange={(e) => {
            const file = e.target.files?.[0] || null;
            updateHtmlFile(file);
            setHtmlFile(file);
          }}
        />
        <label htmlFor="htmlUpload" className={styles.uploadLabel}>
          Выбрать HTML файл
        </label>

        {htmlFile && (
          <div className={styles.fileRow}>
            <span>{htmlFile.name}</span>
            <button
              onClick={() => {
                updateHtmlFile(null);
                setHtmlFile(null);
              }}
            >
              <MdClose />
            </button>
          </div>
        )}
      </div>

      <div className={styles.fileContainer}>
        <p>Загрузите CSS файл(ы)</p>
        <input
          type="file"
          accept=".css"
          multiple
          className={styles.hiddenInput}
          id="cssUpload"
          onChange={(e) => {
            const files = e.target.files ? Array.from(e.target.files) : [];
            updateCssFileList(files);
            setCssFiles(files);
          }}
        />
        <label htmlFor="cssUpload" className={styles.uploadLabel}>
          Выбрать CSS файл(ы)
        </label>

        {cssFileList.length > 0 && (
          <div>
            {cssFileList.map((file, index) => (
              <div key={index} className={styles.fileRow}>
                <span>{file.name}</span>
                <button
                  onClick={() => {
                    const newList = cssFileList.filter((_, i) => i !== index);
                    updateCssFileList(newList);
                    setCssFiles(newList);
                  }}
                >
                  <MdClose />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      <button className={styles.submit} onClick={handleAudit}>
        Проанализировать
      </button>

      {errorMessage && <div className={styles.error}>{errorMessage}</div>}
    </div>
  );
};

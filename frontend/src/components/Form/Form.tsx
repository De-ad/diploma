import { useState } from "react";
import {
  getWebsiteNameFromURL,
  validateURL,
} from "../../utils/checkWebsiteURL";
import { useNavigate } from "react-router";
import { HOME_PAGE_MESSAGE } from "../../constants/text";
import styles from "./styles.module.css";
import ImageUploading, { ImageListType } from "react-images-uploading";
import { sendData, sendURL } from "../../api/auditApi";

type Props = {
  setWebsiteURL: React.Dispatch<React.SetStateAction<string>>;
  websiteURL: string;
  handleAudit: () => Promise<void>;
  errorMessage: string;
};

export const Form = ({
  setWebsiteURL,
  websiteURL,
  handleAudit,
  errorMessage,
}: Props) => {
  const [websiteImages, setWebsiteImages] = useState([]);
  const maxNumber = 10;

  const handleImageChange = (
    imageList: ImageListType,
    addUpdateIndex: number[] | undefined,
  ) => {
    // data for submit
    console.log(imageList, addUpdateIndex);
    setWebsiteImages(imageList as never[]);
  };

  return (
    <div className={styles.block}>
      <p>{HOME_PAGE_MESSAGE}</p>
      <div className={styles.analysis_options}>
        <input
          placeholder="Введите URL сайта"
          onChange={(e) => setWebsiteURL(e.target.value)}
          value={websiteURL}
        ></input>
        <p>Анализ дизайна по визуальному представлению (до 10 изображений):</p>
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
            <div>
              <button
                style={isDragging ? { color: "red" } : undefined}
                onClick={onImageUpload}
                {...dragProps}
              >
                Выбрать файл
              </button>
              &nbsp;
              <button onClick={onImageRemoveAll}>Удалить все файлы</button>
              <div className={styles.uploaded_images_block}>
                {imageList.map((image, index) => (
                  <div key={index}>
                    <img src={image.dataURL} alt="" width="100" />
                    <div className={styles.images_buttons}>
                      <button onClick={() => onImageUpdate(index)}>
                        Изменить
                      </button>
                      <button onClick={() => onImageRemove(index)}>
                        Удалить
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </ImageUploading>

        <p>Анализ дизайна по коду html и css:</p>
        <input
          type="file"
          id="websiteImages"
          name="websiteImages"
          accept=".html, .css"
          multiple
        />
        <button onClick={handleAudit}>Проанализировать</button>
        <div>{errorMessage}</div>
      </div>
    </div>
  );
};

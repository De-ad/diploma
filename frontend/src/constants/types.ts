interface ErrorResult {
  error: string;
}

interface CheckResult {
  found: boolean;
  message: string;
  statusCode: number;
}

interface Metadata {
  titleValue: string | null;
  titleFound: boolean;
  descriptionValue: string | null;
  descriptionFound: boolean;
}

interface SearchPreview {
  url: string;
  title: string | null;
  description: string | null;
  hasFavicon: boolean;
  date: Date | null;
}
type Socials = {
  titleValue?: string | null;
  titleFound: boolean;
  typeValue?: string | null;
  typeFound: boolean;
  descriptionValue?: string | null;
  descriptionFound: boolean;
  imageValue?: string | null;
  imageFound: boolean;
  urlValue?: string | null;
  urlFound: boolean;
  twitterValue?: string | null;
  twitterFound: boolean;
};

export interface SeoResult {
  robots: CheckResult | ErrorResult;
  favicon: CheckResult | ErrorResult;
  sslCertificate: CheckResult | ErrorResult;
  metadata: Metadata | ErrorResult;
  socials: Socials | ErrorResult;
  searchPreview: SearchPreview;
}

export interface WordCloudResult {
  image: string;
}

export interface Performance {
  performanceScore: number;
  firstContentfulPaint: number;
  largestContentfulPaint: number;
  cumulativeLayoutShift: number;
  totalBlockingTime: number;
}

export interface Analysis {
  seo: SeoResult;
  wordcloud: WordCloudResult | ErrorResult;
  performance: Performance | ErrorResult;
}

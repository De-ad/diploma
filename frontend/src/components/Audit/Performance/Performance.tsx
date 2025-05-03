type Props = {
  performance: Performance;
};

export const Performance = ({ performance }: Props) => {
  return (
    <>
      <p>{performance.performanceScore}</p>
      <p>{performance.firstContentfulPaint}</p>
      <p>{performance.largestContentfulPaint}</p>
      <p>{performance.cumulativeLayoutShift}</p>
      <p>{performance.totalBlockingTime}</p>
    </>
  );
};

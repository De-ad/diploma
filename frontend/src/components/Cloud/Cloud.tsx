import React, { useEffect, useRef, useState } from "react";
import * as d3 from "d3";
import cloud, { Word } from "d3-cloud";
import { schemeCategory10 } from "d3-scale-chromatic";
import styles from "./styles.module.css";
type WordData = {
  text: string;
  value: number;
};

type CloudWord = Word & {
  text: string;
  size: number;
  x: number;
  y: number;
  rotate: number;
};

interface WordCloudProps {
  words: WordData[];
}

export const Cloud: React.FC<WordCloudProps> = ({ words }) => {
  const [cloudWords, setCloudWords] = useState<CloudWord[]>([]);
  const svgRef = useRef<SVGSVGElement | null>(null);
  const purpleShades = [
    "#8f00ff",
    "#b611dc",
    "#5a189a",
    "#7b2cbf",
    "#9d4edd",
    "#c77dff",
    "#e0aaff",
  ];
  useEffect(() => {
    const fontScale = d3
      .scaleLinear()
      .domain(d3.extent(words, (d) => d.value) as [number, number])
      .range([10, 60]);

    const layout = cloud()
      .size([500, 400])
      .words(words.map((d) => ({ text: d.text, size: d.value })))
      .padding(1)
      .rotate(() => 0)
      .font("Impact")
      .fontSize((d) => fontScale(d.size ?? 10))
      .on("end", (output: Word[]) => {
        setCloudWords(output as CloudWord[]);
      });

    layout.start();
  }, [words]);

  useEffect(() => {
    if (!svgRef.current) return;
    const svg = d3.select(svgRef.current);
    svg.selectAll("*").remove();

    svg
      .attr("width", 500)
      .attr("height", 400)
      .append("g")
      .attr("transform", "translate(250,200)")
      .selectAll("text")
      .data(cloudWords)
      .enter()
      .append("text")
      .style("font-size", (d) => `${d.size}px`)
      .style("font-family", "Impact")
      .style(
        "fill",
        () => purpleShades[Math.floor(Math.random() * purpleShades.length)],
      )
      .style("cursor", "pointer") // make cursor a pointer
      .attr("text-anchor", "middle")
      .attr("transform", (d) => `translate(${d.x},${d.y}) rotate(${d.rotate})`)
      .text((d) => d.text)
      .on("mouseover", function (event, d) {
        d3.select(this).style("fill", "black"); // highlight color
      })
      .on("mouseout", function (event, d) {
        d3.select(this)
          .style(
            "fill",
            () => purpleShades[Math.floor(Math.random() * purpleShades.length)],
          )
          .style("text-decoration", "none");
      })
      .append("title")
      .text((d) => `Value: ${d.size}`);
  }, [cloudWords]);

  useEffect(() => {
    if (!svgRef.current) return;
    const svg = d3.select(svgRef.current);

    const zoom = d3.zoom().on("zoom", (event) => {
      svg.select("g").attr("transform", event.transform);
    });

    svg.call(zoom);
  }, []);

  return (
    <div className={styles.container}>
      <h2>Облако слов</h2>
      <svg ref={svgRef}></svg>
    </div>
  );
};

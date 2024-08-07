import styled from 'styled-components';
import * as d3 from 'd3';
import React, { useRef, useEffect } from 'react';
import styles from './styles.module.css';


const StyledSVG = styled.svg`
  .link {
    fill: none;
    stroke: steelblue;
    stroke-width: 2px;
  }
`;

const Tree: React.FC = () => {
  const svgRef = useRef<SVGSVGElement>(null);
    

  useEffect(() => {
    const margin = { top: 20, right: 120, bottom: 20, left: 120 };
    const width = 960 - margin.right - margin.left;
    const height = 500 - margin.top - margin.bottom;

    // Cleanup any existing content in the SVG before appending new elements
    d3.select(svgRef.current).selectAll('*').remove();

    const svg = d3.select(svgRef.current)
      .attr('width', width + margin.right + margin.left)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    const treemap = d3.tree().size([height, width]);

    const data = {
      name: "Root",
      children: [
        { name: "Child 1" },
        {
          name: "Child 2",
          children: [
            { name: "Grandchild 2.1" },
            { name: "Grandchild 2.2" }
          ]
        },
        { name: "Child 3" }
      ]
    };

    const root = d3.hierarchy(data, d => (d as any).children);
    const treeData = treemap(root as any);

    const nodes = treeData.descendants();
    const links = treeData.descendants().slice(1);

    nodes.forEach(d => d.y = d.depth * 180);

    svg.selectAll('path.link')
      .data(links)
      .enter().append('path')
      .attr('class', styles.link)
      .attr('d', d => {
        const line = d3.line()
          .curve(d3.curveBasis)
          .x(d => d[0])
          .y(d => d[1]);

        return line([
          [(d as any).parent.y, (d as any).parent.x],
          [((d as any).parent.y + d.y) / 2, (d as any).parent.x],
          [((d as any).parent.y + d.y) / 2, d.x],
          [d.y, d.x]
        ]);
      });

    const node = svg.selectAll('g.node')
      .data(nodes)
      .enter().append('g')
      .attr('class', styles.node)
      .attr('transform', d => `translate(${d.y},${d.x})`);

      // Append background rect
    node.append('rect')
    .attr('x', d => d.children ? -60 : -3)
    .attr('y', 0)
    .attr('width', d => d.children ? 150 : 150); // Adjust width as needed

    node.append('text')
      .attr('dy', '.35em')
      .attr('x', d => d.children ? 13 : 13)
      .attr('text-anchor', d => d.children ? 'end' : 'start')
      .text(d => (d as any).data.name);
      
  }, []); // Ensure this runs only once by using an empty dependency array


  return (
    <StyledSVG ref={svgRef} className={styles.wrapper}></StyledSVG>
  );
};

export default Tree;

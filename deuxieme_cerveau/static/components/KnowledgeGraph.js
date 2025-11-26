const KnowledgeGraph = ({ notes }) => {
  const svgRef = React.useRef(null);
  const wrapperRef = React.useRef(null);

  React.useEffect(() => {
    try {
      if (!notes || !notes.length || !svgRef.current || !wrapperRef.current) return;

      // 1. Data Preparation
      const nodes = [];
      const links = [];
      const tagMap = new Map();

      notes.forEach(note => {
        nodes.push({
          id: note.id,
          label: note.summary.slice(0, 15) + '...',
          group: 1,
          r: 8
        });

        note.tags.forEach(tag => {
          const tagId = `tag-${tag}`;
          if (!tagMap.has(tag)) {
            tagMap.set(tag, tagId);
            nodes.push({
              id: tagId,
              label: tag,
              group: 2,
              r: 5
            });
          }
          links.push({
            source: note.id,
            target: tagId,
            value: 1
          });
        });
      });

      // 2. D3 Configuration
      const width = wrapperRef.current.clientWidth;
      const height = wrapperRef.current.clientHeight;

      const svg = d3.select(svgRef.current);
      svg.selectAll("*").remove();

      const g = svg.append("g");

      const zoom = d3.zoom()
        .scaleExtent([0.1, 4])
        .on("zoom", (event) => {
          g.attr("transform", event.transform);
        });

      svg.call(zoom);

      const simulation = d3.forceSimulation(nodes)
        .force("link", d3.forceLink(links).id(d => d.id).distance(80))
        .force("charge", d3.forceManyBody().strength(-200))
        .force("center", d3.forceCenter(width / 2, height / 2))
        .force("collide", d3.forceCollide().radius(20));

      const link = g.append("g")
        .attr("stroke", "#475569")
        .attr("stroke-opacity", 0.6)
        .selectAll("line")
        .data(links)
        .join("line")
        .attr("stroke-width", d => Math.sqrt(d.value));

      const node = g.append("g")
        .selectAll("g")
        .data(nodes)
        .join("g")
        .call(d3.drag()
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended));

      node.append("circle")
        .attr("r", d => d.group === 1 ? 12 : 6)
        .attr("fill", d => d.group === 1 ? "#0ea5e9" : "#f472b6")
        .attr("stroke", "#fff")
        .attr("stroke-width", 1.5);

      node.append("text")
        .text(d => d.label)
        .attr("x", 15)
        .attr("y", 4)
        .style("font-size", "10px")
        .style("fill", "#cbd5e1")
        .style("pointer-events", "none");

      simulation.on("tick", () => {
        link
          .attr("x1", d => d.source.x)
          .attr("y1", d => d.source.y)
          .attr("x2", d => d.target.x)
          .attr("y2", d => d.target.y);

        node
          .attr("transform", d => `translate(${d.x},${d.y})`);
      });

      function dragstarted(event, d) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
      }

      function dragged(event, d) {
        d.fx = event.x;
        d.fy = event.y;
      }

      function dragended(event, d) {
        if (!event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
      }

      return () => {
        simulation.stop();
      };
    } catch (error) {
      console.error('Error rendering knowledge graph:', error);
    }
  }, [notes]);

  return (
    <div ref={wrapperRef} className="w-full h-full bg-slate-900 overflow-hidden relative rounded-xl border border-slate-700">
      <div className="absolute top-4 left-4 z-10 bg-slate-800/80 p-2 rounded text-xs text-slate-300">
        <div className="flex items-center gap-2 mb-1"><span className="w-2 h-2 rounded-full bg-sky-500"></span> Note</div>
        <div className="flex items-center gap-2"><span className="w-2 h-2 rounded-full bg-pink-400"></span> Tag</div>
      </div>
      <svg ref={svgRef} className="w-full h-full cursor-move" />
    </div>
  );
};

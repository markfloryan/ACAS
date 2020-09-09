//Overrides the default node generation system in favor of one that ignores competency

//Creates an SVG representation of the node.
export const generate_svg = (svg, title, competency, lock) => {

  let status = '';
  let color = '#90EE90';
  let competencyMessage = '';

  //Truncate long titles.
  if (title && title.length > 12) {
    title = title.substring(0, 13) + '...';
  }

  const SVG =
  `<svg width="230pt" height="102pt" viewBox="0 0 230 136" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
    <!-- Generator: Sketch 49.3 (51167) - http://www.bohemiancoding.com/sketch -->
    <desc>Created with Sketch.</desc>
    <defs>
      <rect id="path-1" x="0" y="0" width="222" height="128" rx="7"></rect>
      <filter x="-2.3%" y="-3.9%" width="106.3%" height="110.9%" filterUnits="objectBoundingBox" id="filter-2">
        <feOffset dx="2" dy="2" in="SourceAlpha" result="shadowOffsetOuter1"></feOffset>
        <feGaussianBlur stdDeviation="2" in="shadowOffsetOuter1" result="shadowBlurOuter1"></feGaussianBlur>
        <feComposite in="shadowBlurOuter1" in2="SourceAlpha" operator="out" result="shadowBlurOuter1"></feComposite>
        <feColorMatrix values="0 0 0 0 0   0 0 0 0 0   0 0 0 0 0  0 0 0 0.5 0" type="matrix" in="shadowBlurOuter1"></feColorMatrix>
      </filter>
    </defs>
    <g id="Wireframes" stroke="none" stroke-width="1" fill="${ color }" fill-rule="evenodd" opacity="1">
      <g id="Dash---Class-selected" transform="translate(-794.000000, -369.000000)">
        <g id="main-content" transform="translate(262.000000, 128.000000)">
          <g id="content" transform="translate(46.000000, 23.000000)">
            <g id="class" transform="translate(488.000000, 220.000000)">
              <g id="Rectangle">
                <use fill="black" fill-opacity="1" filter="url(#filter-2)" xlink:href="#path-1"></use>
                <use fill="#FFFFFF" fill-rule="evenodd" xlink:href="#path-1"></use>
                <rect stroke="#979797" stroke-width="1" x="0.5" y="0.5" width="221" height="127" rx="7"></rect>
              </g>
              <text id="Not-unlocked" font-family="Helvetica" font-size="14" font-weight="normal" letter-spacing="3.3" fill="#000000">
                <tspan x="18.6921875" y="113">${ competencyMessage }</tspan>
              </text>
              <text id="Not-unlocked" font-family="Helvetica" font-size="14" font-weight="normal" letter-spacing="3.3" fill="#000000">
                <tspan x="145" y="29">${ status }</tspan>
              </text>
              <text id="TopicName" font-family="Helvetica" font-size="18" font-weight="normal" letter-spacing="3.29999995" fill="#000000">
                <tspan x="12" y="29">${ title }</tspan>
              </text>
            </g>
          </g>
        </g>
      </g>
    </g>
  </svg>`;

  return SVG;
};

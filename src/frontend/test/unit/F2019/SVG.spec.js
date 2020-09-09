import Vuex from 'vuex';

import {generate_svg, perc2color} from '@/assets/graph_node_svg.js';

describe('graph_node_svg.js', () => {

	let node_nc = {
		name: 'not competent',
		grade: 0,
		locked: false,
	};
	let node_sc = {
		name: 'not competent',
		grade: 60,
		locked: false,
	};
	let node_fc = {
		name: 'not competent',
		grade: 90,
		locked: false,
	};



	it('generate_svg: displays correct competency', () => {
		let svg_nc = generate_svg(null, node_nc.name, node_nc.grade, node_nc.locked);
		let svg_sc = generate_svg(null, node_sc.name, node_sc.grade, node_sc.locked);
		let svg_fc = generate_svg(null, node_fc.name, node_fc.grade, node_fc.locked);

		expect(svg_nc.includes("N.C.")).to.equal(true);
		expect(svg_sc.includes("S.C.")).to.equal(true);
		expect(svg_fc.includes("F.C.")).to.equal(true);
	})
});

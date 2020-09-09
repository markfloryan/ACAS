<template>
  <!-- ClassGraph.vue
    This component is the actual component for the graph of nodes that represents
    a course
  -->
  <div class="class-graph">
    <network ref="network"
      :edges="edges"
      :nodes="nodes"
      :options="options"
      :events="['click', 'dragStart', 'dragEnd', 'hoverNode', 'blurNode']"
      @click="clickTest"
      @drag-start="mousedownOnCanvas"
      @drag-end="mouseUpOnCanvas"
      @hover-node="hoverNode"
      @blur-node="blurNode"
      class="network"
      :style="canvasStyle">
    </network>
    <TopicModal
      :isOpen="topicModalIsOpen"
      :role="role"
      :data="selectedNodeData"
      @onClose="topicModalIsOpen = false; $emit('onClose');" />
  </div>
</template>

<script>
import { Network } from 'vue2vis';
import { generate_svg } from '@/assets/graph_node_svg.js';
import { edges, nodes as nodeData, options } from '@/assets/test_graph_data.js';
import TopicModal from '@/components/TopicModal';

export default {
  components: {
    Network,
    TopicModal,
  },
  props: {
    data: {},
    role: {
      type: String,
    }
  },
  data() {
    return {
      network: null,
      layoutMethod: 'directed',
      edges: [],
      nodes: [],
      options: {},
      selectedNodeData: {},
      topicModalIsOpen: false,
      canvasStyle: {
        cursor: ' -webkit-grab'
      },
    };
  },
  methods: {
    // opens the modal for the clicked topic
    clickTest(data) {
      // this.selectedNodeData = data;
      this.nodes.forEach((node) => {
        if (data.nodes && data.nodes[0] === node.id) {
          this.topicModalIsOpen = true;
          this.selectedNodeData = node;
        }
      });
    },
    // generates the actual markup for the graph
    generate_custom_graph_markup(nodeData) {
      const SVG = generate_svg();
      let nodes = nodeData;

      let nodeImage;
      nodes.forEach((node) => {
        nodeImage = generate_svg(SVG, node.topic.name, node.competency, node.topic.locked);
        node.shape = 'image';
        node.image = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(nodeImage);
        node.id = node.topic.id;
      });

      return nodes;
    },
    // Style only: changes the look of the mouse when interacting with the canvas
    mousedownOnCanvas() {
      this.canvasStyle = {
        cursor: ' -webkit-grabbing'
      };
    },
    // Style only: changes the look of the mouse when interacting with the canvas
    mouseUpOnCanvas() {
      this.canvasStyle = {
        cursor: ' -webkit-grab'
      };
    },
    // Style only: changes the look of the mouse when interacting with the canvas
    hoverNode() {
      this.canvasStyle = {
        cursor: 'pointer'
      };
    },
    // Style only: changes the look of the mouse when interacting with the canvas
    blurNode() {
      this.canvasStyle = {
        cursor: '-webkit-grab'
      };
    },
  },
  watch: {
    // WHen the component recieves an updated version of the 'data' prop, this runs
    // and updates the other vars related to the 'data' prop
    data(newData) { // runs when data prop is updated

      // builds the graph if the user is a professor; ignores whether or not the
      // topics are locked
      if (newData.edges && newData.nodes && newData.nodes[0].student.is_professor) {
        this.edges = newData.edges.map((edge) => {
          return { from: edge.ancestor_node, to: edge.topic_node};
        });
        this.nodes = this.generate_custom_graph_markup(newData.nodes);
        this.options = options(this.layoutMethod);
      }
      // builds the graph if the user is not a professor; only displays unlocked
      // topics
      else if(newData.edges && newData.nodes) {
        this.edges = newData.edges.map((edge) => {
          return { from: edge.ancestor_node, to: edge.topic_node};
        });
        // var tempNodes = []
        // newData.nodes.forEach((node) => {
        //   if(!node.locked) {
        //     tempNodes.push(node)
        //   }
        // });
        this.nodes = this.generate_custom_graph_markup(newData.nodes.filter((node) => !node.topic.locked));
        this.options = options(this.layoutMethod);
      }
    }
  },
};
</script>

<style scoped>
  .class-graph {
    height: 100%;
    position: relative;
  }
  .network {
    height: 100%;
  }

</style>

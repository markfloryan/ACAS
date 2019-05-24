<template>
  <div v-if="isOpen" class="topic-modal" @click.self="closeModal()">
    <div class="content">
      <h1 style="border-bottom: solid 0.75pt lightgray; padding-bottom: 8pt;">Create a new topic node:</h1>
      <sui-form @submit.prevent>
        <sui-form-field>
          <label>Topic name</label>
          <input v-model="tname" placeholder="Topic name" type="text">
        </sui-form-field>
        <div style="text-align: center;">
          <button type="button" @click="closeModal()" style="margin-right: 8pt;" class="btn btn-plain cancel-btn">Cancel</button>
          <button type="button" @click="createTopic()" class="btn btn-create create-btn">Create</button>
        </div>
      </sui-form>
      <p v-show="aexist === true">*Already Exists</p>
    </div>
  </div>
</template>

<script>
import { generate_svg } from '@/assets/graph_node_svg.js';
export default {
  name: 'EditPopup',
  components: {
    
  },
  props: {
    data: {
      type: Object,
    },
    isOpen: {
      type: Boolean,
      required: false,
    },
    nodes: {
      type: Array,
    },
    edges: {
      type: Array,
    },
    classData: {
      type: Object
    }
  },
  data() {
    return {
      tname: '',
      tid: '',
      aexist:false,
    };
  },
  created() {
    // console.log(this.data);
  },
  methods: {
    closeModal(event) {
      this.$emit('onClose');
    },
    createTopic(event) {
      this.aexist=false;
      //check if name already exists
      this.nodes.forEach(node=>{
        if(node.topic.name == this.tname){
          this.aexist = true;
        }
      });
      //if not create
      if(this.aexist === false){
        const SVG = generate_svg();
        let nodeImage;
        let node = {'course':this.classData,'grade':0,'id':this.tid,'locked':false,'student':{},'topic':{'course':this.classData.uuid,'id':'None','name':this.tname}};
        nodeImage = generate_svg(SVG, node.topic.name, node.grade, node.locked);
        node.shape = 'image';
        node.image = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(nodeImage);
        this.tid += 'a';
        this.nodes.push(node);
        this.tname = '';
        this.$emit('onClose');
      }
      else{
        return;
      }
    }
  }
};
</script>

<style scoped>
  .topic-modal {
    position: absolute;
    top: 0;
    left: 0;
    z-index: 1000000;
    width: 100%;
    height: 100%;
    background-color: rgba(100, 100, 100, 0.8);
  }
  .topic-modal > .content {
    grid-area: content;
    background-color: #fff;
    -webkit-box-shadow: 0 0.75pt 1.5pt 0 rgba(34,36,38,.15);
    box-shadow: 0 0.75pt 1.5pt 0 rgba(34,36,38,.15);
    border: 0.75pt solid rgba(34,36,38,.15);
    padding: 8pt;
    border-radius: 6pt;
    
    margin: auto;
    width: 300pt;
    min-width: 225pt;
    height: min-content;
    position: relative;
    top: 50%;
    transform: perspective(0.75pt) translateY(-50%);
    padding: 18pt;
  }
  .topic-modal > .content > .title {
    grid-area: title;
  }
  .topic-modal > .content > .tab-nav {
    grid-area: tabnav;
  }
  .topic-modal > .content > .main {
    grid-area: main;
  }
  .close-modal-button {
    cursor: pointer;
    grid-area: exit;
  }
  .close-modal-button:hover {
    color: var(--color-blue);
  }
</style>
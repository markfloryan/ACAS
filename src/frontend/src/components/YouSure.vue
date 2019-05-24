<template>
  <div v-if="isOpen" class="topic-modal" @click.self="closeModal()">
    <div class="content">
      <h1 style="border-bottom: solid 0.75pt lightgray; padding-bottom: 8pt;">Delete Node?</h1>
      
        <div style="text-align: center;">
          <button type="button" @click="closeModal()" style="margin-right: 8pt;" class="btn btn-plain cancel-btn">Cancel</button>
          <button type="button" @click="confirmModal()" class="btn btn-create create-btn">Confirm</button>
        </div>
    </div>
  </div>
</template>

<script>
import { generate_svg } from '@/assets/graph_node_svg.js';

export default {
  name: 'YouSure',
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
  },
  data() {
    return {
      tname: '',
      tid: '',
    };
  },
  created() {
    // console.log(this.data);
  },

  methods: {
    closeModal(event) {
      this.$emit('closeConfirm');
      console.log('close');
    },
    confirmModal(event) {
      this.$emit('confirm');
      console.log('confrim');
      this.$emit('closeConfirm');
    },
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
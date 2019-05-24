<template>
  <div class="main">
    <sui-form v-if="role === 'professor'" @submit.prevent>
      <sui-form-field>
        <label>Name:</label>
        <input placeholder="Name" v-model="newResource.name">
      </sui-form-field>
      <sui-form-field>
        <label>URL</label>
        <input placeholder="URL" v-model="newResource.link">
      </sui-form-field>
      <br>
      <button type="button" class="btn btn-create" @click="addResource">Add resource</button>
    </sui-form>
    <div v-if="resources.length > 0" style="margin-top: 8pt; overflow-y: scroll"
      :style="{ height: role === 'professor' ? '225pt' : '375pt' }">
      <sui-table celled >
        <sui-table-header>
          <sui-table-row>
            <sui-table-header-cell :width="4">Name</sui-table-header-cell>
            <sui-table-header-cell :width="10">Link</sui-table-header-cell>
            <sui-table-header-cell :width="2"
              v-if="role === 'professor'">Actions</sui-table-header-cell>
          </sui-table-row>
        </sui-table-header>
        <sui-table-body>
          <sui-table-row v-for="(resource,n) in resources" :key="`${resource.link}-${n}-tab`">
            <sui-table-cell>{{ resource.name }}</sui-table-cell>
            <sui-table-cell >
              <a target="blank" :href="resource.link">{{ resource.link.length > 100 ? `${resource.link.substring(0, 100)}...` : resource.link }}</a>
            </sui-table-cell>
            <sui-table-cell  v-if="role === 'professor'">
              <button @click="removeResource(n)">Remove</button>
            </sui-table-cell>
          </sui-table-row>
        </sui-table-body>
      </sui-table>
    </div>
    <h2 v-else>
      No resources for this topic yet
    </h2>
  </div>
</template>

<script>
import axios from 'axios';
import { mapGetters, mapMutations } from 'vuex';
import { API_URL } from '@/constants';

export default {
  components: {
    
  },
  props: {
    role: {
      type: String,
      default: 'professor',
    },
    data: {
      type: Object,
    },
    topicId: {
      type: Number,
    },
  },
  data() {
    return {
      resources: [
      ],
      newResource: {
        name: '',
        link: '',
      },
    };
  },
  mounted() {
    this.retrieveResources();
  },
  methods: {
    ...mapMutations('toast', ['openToast', 'setToastInfo']),
    retrieveResources() {
      axios.get(`${API_URL}/resources/${this.topicId}`)
        .then((resources) => {
          this.resources = resources.data.result;
        });
    },

    addResource(){
      if(!this.newResource.name || !this.newResource.link){
        this.openToast();
        this.setToastInfo({
          type: 'error',
          title: 'Couldn\'t add the resource!',
          message: 'Please provide both a name and URL for the resource.',
          duration: 6000,
        });
      } else {

        const resourceData = {
          name: this.newResource.name,
          link: this.newResource.link,
          topic: this.data.topic.id
        };

        axios.post(`${API_URL}/resources/`, resourceData)
          .then((response) => {
            this.openToast();
            this.setToastInfo({
              type: 'success',
              title: 'Resource added!',
              duration: 6000,
            });
          })
          .catch((error) => {
            this.openToast();
            this.setToastInfo({
              type: 'error',
              title: 'Couldn\t add the resource!',
              message: 'There was an issue on our end, please try again later.',
              duration: 6000,
            });
          })
          .finally(() => {
            this.newResource.name = '';
            this.newResource.link = '';
            this.retrieveResources();
          });
      }
    },

    removeResource(n) {
      axios.delete(`${API_URL}/resources/${this.resources[n].pk}`)
        .then((response) => {      
          this.openToast();
          this.setToastInfo({
            type: 'success',
            title: 'Resource successfully removed!',
            duration: 6000,
          });
        })
        .catch((error) => {
          this.openToast();
          this.setToastInfo({
            type: 'error',
            title: 'Couldn\t remove the resource!',
            message: 'There was an issue on our end, please try again later.',
            duration: 6000,
          });
        })
        .finally(() => {
          this.retrieveResources();
        }); 
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
    width: 70%;
    min-width: 525pt;
    height: 95%;

    position: relative;
    top: 50%;
    transform: perspective(0.75pt) translateY(-50%);
    padding: 18pt;

    display: grid;
    grid-template-areas: 
    'title exit'
    'tabnav tabnav'
    'main main';
    grid-template-rows: min-content min-content 1fr;
    grid-template-columns: 1fr min-content;
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
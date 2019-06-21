<template>
  <div class="main">
    <h1>Ancestor Weights</h1>
    <p>This value represents how the total of all ancestor nodes will be weighted in the topic grade. The more that the ancestors are weighted, the less the assignments and grades in the topic influence the grade of the topic.</p>
    <p>The weights of the ancestor nodes can be factored into the current topics weight. The grades are calculated using a weighted sum.</p>
    <p>Acceptable values are 0 - 1</p>
    <sui-form v-if="role === 'professor'" @submit.prevent>
      <sui-form-field>
        <label>Ancestor Weight</label>
        <input
          v-bind:placeholder="'Current ancestor weight is: '+  this.data.topic.ancestor_weight"
          v-model="newTopic.weight"
          type="number"
        >
      </sui-form-field>
      <button
        type="button"
        class="btn btn-create"
        @click="updateTopicWeight()"
      >Update Ancestor Weight</button>
    </sui-form>
    <br>
    <div v-if="this.ancestors.length == 0">This node does not inherit from any other nodes</div>
    <div v-else>
      <p>You can customize the weight that each ancestor has. This is the percentage of influence that each individual ancestor has on the ancestor weight (entered above)</p>
      <p>Please ensure that the total weight of all nodes sums to one. To update the weights, all inputs must have a value</p>
      <p>Acceptable values are 0 - 1</p>
      <sui-table celled v-if="role === 'professor'">
        <sui-table-header>
          <sui-table-row>
            <sui-table-header-cell :width="5">Ancestor Topic</sui-table-header-cell>
            <sui-table-header-cell :width="5">Weight</sui-table-header-cell>
          </sui-table-row>
        </sui-table-header>
        <sui-table-body>
          <sui-table-row v-for="(node,n) in ancestors" :key="`${n}-tab`">
            <sui-table-cell>{{ node.ancestor_name }}</sui-table-cell>
            <sui-table-cell>
              <input
                type="number"
                :placeholder="'Current weight: ' + node.weight"
                v-model="form.weight[n]"
                :id="n"
              >
            </sui-table-cell>
          </sui-table-row>
        </sui-table-body>
      </sui-table>
      <sui-form v-if="role === 'professor'" @submit.prevent>
        <button type="button" class="btn btn-create" @click="updateTopicWeights()">Update Weights</button>
      </sui-form>
    </div>
    <h1>Topic Categories</h1>
    <p>Each topic to category relationship creates a relatonship between a topic and a category. This allows for grades to fall into one of these categories and have a certain weight associated to the overall grade of a topic. Thus a topic to category with a weight of 0.25 will account for 25% of the grade of the topic</p>
    <p>Each topic has its own relationship with a category to provide the most custimization possible</p>
    <sui-form v-if="role === 'professor'" @submit.prevent>
      <sui-form-field>
        <!-- https://semantic-ui-vue.github.io/#/modules/dropdown -->
        <label>Category</label>
        <sui-dropdown
          placeholder="Category"
          selection
          :options="this.categories"
          v-model="newTopicToCategory.category"
        />
        <!-- <input placeholder="URL" v-model="newTopicToCategory.category"> -->
      </sui-form-field>
      <sui-form-field>
        <label>Weight</label>
        <input placeholder=".25" v-model="newTopicToCategory.weight" type="number">
      </sui-form-field>
      <br>
      <button type="button" class="btn btn-create" @click="addTopicToCategory()">Add Topic Category</button>
    </sui-form>
    <div
      v-if="topicToCategory.length > 0"
      style="margin-top: 8pt; overflow-y: scroll"
      :style="{ height: role === 'professor' ? '225pt' : '375pt' }"
    >
      <sui-table celled>
        <sui-table-header>
          <sui-table-row>
            <sui-table-header-cell :width="4">Category</sui-table-header-cell>
            <sui-table-header-cell :width="10">Weight</sui-table-header-cell>
            <sui-table-header-cell :width="2" v-if="role === 'professor'">Action</sui-table-header-cell>
          </sui-table-row>
        </sui-table-header>
        <sui-table-body>
          <sui-table-row v-for="(topic,n) in topicToCategory" :key="`${topic.category}-${n}-tab`">
            <sui-table-cell>{{ topic.category }}</sui-table-cell>
            <sui-table-cell>{{ topic.weight }}</sui-table-cell>
            <sui-table-cell v-if="role === 'professor'">
              <button @click="removeTopicToCategory(n)">Remove</button>
            </sui-table-cell>
          </sui-table-row>
        </sui-table-body>
      </sui-table>
    </div>
    <h2 v-else>No categories to show</h2>
  </div>
</template>

<script>
import axios from 'axios';
import { mapGetters, mapMutations } from 'vuex';
import { API_URL } from '@/constants';

export default {
  components: {},
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
      categories: [],
      topicToCategory: [],
      newTopicToCategory: {
        category: '',
        weight: null,
      },
      newTopic: {
        weight: 0,
      },
      ancestors: [],
      form: {
        weight: [],
      },
    };
  },
  mounted() {
    this.retrieveCategories();
    this.retrieveTopicToCategories();
    this.getTopicAncestors();
    this.newTopic.weight = this.data.topic.ancestor_weight;
  },
  created() {
    //this.context='quiz';
    // console.log(this.data);
  },
  methods: {
    ...mapMutations('toast', ['openToast', 'setToastInfo']),
    closeModal(event) {
      this.$emit('onClose');
    },
    // Gets all of the weights that were inputted from the form
    updateTopicWeights() {
      // Loop through the different models and update the topic to categories

      // Little bit of error handling
      let total_weight = 0;
      for (let i = 0; i < this.form.weight.length; i++) {
        const weight = this.form.weight[i];
        // console.log(parseFloat(this.form.weight[i]));
        total_weight += parseFloat(weight);
      }

      // If the total weight is > 1, then we dont let them post
      if (total_weight > 1) {
        // Toast
        this.openToast();
        this.setToastInfo({
          type: 'error',
          title: 'Update Error',
          message: 'Please ensure the weights sum to less than 1',
          duration: 6000,
        });
        return;
      }

      for (let index = 0; index < this.form.weight.length; index++) {
        // Weight is the weight of the topic to topic relationship
        const weight = this.form.weight[index];

        // Update the ancestor data
        this.ancestors[index].weight = weight;

        // Update the data through a PUT request
        axios
          .put(
            `${API_URL}/topic/topics/${this.ancestors[index].pk}/`,
            this.ancestors[index]
          )
          // Do nothing
          .then(res => {})
          // Log the error if there is one
          .catch(err => {
            console.log(err);
            // Toast
            this.openToast();
            this.setToastInfo({
              type: 'error',
              title: 'Update Error',
              message: 'There was an error updating the weight',
              duration: 6000,
            });
          });
      }
      // Let them know things changed
      this.openToast();
      this.setToastInfo({
        type: 'success',
        title: 'Weights updated',
        message: 'The weights were successfully updated',
        duration: 6000,
      });
      // Clear the data and get it again
      this.ancestors = [];
      this.getTopicAncestors();
    },
    // Get all available categories
    retrieveCategories() {
      let allCategories = [];
      axios.get(`${API_URL}/categories/`).then(categories => {
        allCategories = categories.data.result;
        // console.log(allCategories);
        for (let i = 0; i < allCategories.length; i++) {
          // console.log(allCategories[i].name);
          allCategories[i] = {
            text: allCategories[i].name,
            value: allCategories[i].name,
          };
        }

        this.categories = allCategories;
        this.categories = this.categories.filter(category => {
          return category.text !== 'Internal Quiz';
        });
      });
    },
    // gets a list of all the topics that are ancestors to the topic
    getTopicAncestors() {
      axios
        .get(`${API_URL}/topic/topics/${this.data.topic.id}/`)
        .then(res => {
          this.ancestors = res.data.result;
        })
        .catch(err => {
          console.log(err);
        });
    },
    // updates the topic weight
    updateTopicWeight() {
      // Some basic error handling
      const weight = parseFloat(this.newTopic.weight);

      // If the total weight is > 1, then we dont let them post
      if (weight > 1) {
        // Toast
        this.openToast();
        this.setToastInfo({
          type: 'error',
          title: 'Update Error',
          message: 'Please ensure the weight is less than 1',
          duration: 6000,
        });
        return;
      }

      let data = {
        name: this.data.topic.name,
        course: this.data.topic.course,
        ancestor_weight: this.newTopic.weight,
      };
      axios
        .put(`${API_URL}/topics/${this.data.topic.id}`, data)
        .then(response => {
          this.getTopicWeight();
          // Let them know things changed
          this.openToast();
          this.setToastInfo({
            type: 'success',
            title: 'Weights updated',
            message: 'The weight was successfully updated',
            duration: 6000,
          });
        })
        .catch(error => {
          console.log(error);
          this.openToast();
          this.setToastInfo({
            type: 'error',
            title: 'Could not update topic weight',
            message: 'Please try again',
            duration: 6000,
          });
        });
    },
    // Get the topic weight
    getTopicWeight() {
      axios
        .get(`${API_URL}/topics/${this.data.topic.id}/`)
        .then(topic => {
          this.newTopic.weight = topic.data.result.ancestor_weight;
          this.data.topic.ancestor_weight = topic.data.result.ancestor_weight;
          // console.log(topic.data.result.weight);
        })
        .catch(function(error) {
          console.log(error);
        });
    },
    // Get all topic to categories for a topic
    retrieveTopicToCategories() {
      axios
        .get(`${API_URL}/topic/category/${this.data.topic.id}/`)
        .then(categories => {
          console.log('other cata data: ', categories.data.result);
          console.log('ID INFO:: ', this.data.topic.id);
          this.topicToCategory = categories.data.result;
          // console.log(this.topicToCategory);
        })
        .catch(function(error) {
          console.log(error);
        });
    },

    addTopicToCategory() {
      // Check to see if the form is correct
      if (
        !this.newTopicToCategory.category ||
        !this.newTopicToCategory.weight
      ) {
        this.openToast();
        this.setToastInfo({
          type: 'error',
          title: 'Could not add category',
          message: 'Please add both fields',
          duration: 6000,
        });
      } else {
        // Create post object
        const categoryData = {
          category: this.newTopicToCategory.category,
          weight: this.newTopicToCategory.weight,
          topic: this.data.topic.id, //pk
        };
        console.log('cat dat : ', categoryData);
        // Post and create
        axios
          .post(`${API_URL}/topic/category/`, categoryData)
          .then(response => {})
          .catch(error => {
            console.log(error);
            this.openToast();
            this.setToastInfo({
              type: 'error',
              title: 'Could not add category',
              message: 'Please make sure the total weights sum to 1 or less',
              duration: 6000,
            });
          })
          .finally(() => {
            // Clear data and update list
            this.newTopicToCategory.category = '';
            this.newTopicToCategory.weight = null;
            this.retrieveCategories();
            this.retrieveTopicToCategories();
          });
      }
    },

    removeTopicToCategory(n) {
      //  Get the list of all topics and categories
      axios
        .get(`${API_URL}/topic/category/${this.data.topic.id}/`)
        .then(categories => {
          this.topicToCategory = categories.data.result;
          // console.log(this.topicToCategory);
          const profile = JSON.parse(localStorage.getItem('profile'));

          // Delete the resource
          axios
            .delete(`${API_URL}/topic/category/${this.topicToCategory[n].pk}/?id_token=${profile.auth.profile.id_token}`)
            .then(function(response) {
              // console.log(response);
            })
            .catch(function(error) {
              console.log(error);
            })
            .finally(() => {
              this.retrieveCategories();
              this.retrieveTopicToCategories();
            });
        });
    },
  },
};
</script>

<style scoped>
.main {
  overflow-y: scroll;
}
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
  -webkit-box-shadow: 0 0.75pt 1.5pt 0 rgba(34, 36, 38, 0.15);
  box-shadow: 0 0.75pt 1.5pt 0 rgba(34, 36, 38, 0.15);
  border: 0.75pt solid rgba(34, 36, 38, 0.15);
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

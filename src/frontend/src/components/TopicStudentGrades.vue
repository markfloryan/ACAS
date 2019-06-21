<template>
  <div class="main">
    <sui-form v-if="role === 'professor'" @submit.prevent>
      <sui-form-field>
        <!-- Description for the grade -->
        <label>Description</label>
        <input type="text" placeholder="Assessment Name" v-model="newTopicToCategory.description">
        <!-- <input placeholder="URL" v-model="newTopicToCategory.category"> -->
      </sui-form-field>
      <sui-form-field>
        <!-- Student who the grade goes to -->
        <!-- https://semantic-ui-vue.github.io/#/modules/dropdown -->
        <label>Student</label>
        <sui-dropdown
          placeholder="Student"
          selection
          :options="this.students"
          v-model="newTopicToCategory.student"
        />
        <!-- <input placeholder="URL" v-model="newTopicToCategory.category"> -->
      </sui-form-field>
      <sui-form-field>
        <!-- https://semantic-ui-vue.github.io/#/modules/dropdown -->
        <label>Category</label>
        <sui-dropdown
          placeholder="Category"
          selection
          :options="this.topicToCategory"
          v-model="newTopicToCategory.category"
        />
        <!-- <input placeholder="URL" v-model="newTopicToCategory.category"> -->
      </sui-form-field>
      <sui-form-field>
        <label>Grade</label>
        <input placeholder="85" v-model="newTopicToCategory.weight" type="number">
      </sui-form-field>
      <br>
      <button type="button" class="btn btn-create" @click="addStudentGrade()">Add Student Grade</button>
    </sui-form>
    <!-- <div
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
            <sui-table-cell>{{topic.weight}}</sui-table-cell>
            <sui-table-cell v-if="role === 'professor'">
              <button @click="removeTopicToCategory(n)">Remove</button>
            </sui-table-cell>
          </sui-table-row>
        </sui-table-body>
      </sui-table>
    </div>
    <h2 v-else>No grades for this topic yet</h2>-->
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
      students: [],
      topicToCategory: [],
      newTopicToCategory: {
        category: '',
        weight: null,
      },
    };
  },
  mounted() {
    this.getAllStudentsInTopic();
    this.retrieveCategories();
    this.retrieveTopicToCategories();
  },
  created() {},
  methods: {
    ...mapMutations('toast', ['openToast', 'setToastInfo']),
    closeModal(event) {
      this.$emit('onClose');
    },
    // Get all available categories
    retrieveCategories() {
      let allCategories = [];
      axios.get(`${API_URL}/categories/`).then(categories => {
        allCategories = categories.data.result;
        for (let i = 0; i < allCategories.length; i++) {
          allCategories[i] = {
            text: allCategories[i].name,
            value: allCategories[i].name,
          };
        }

        this.categories = allCategories;
      });
    },
    // Get all topic to categories for a topic
    retrieveTopicToCategories() {
      axios
        .get(`${API_URL}/topic/category/${this.data.topic.id}/`)
        .then(categories => {
          this.topicToCategory = categories.data.result;
          console.log(this.topicToCategory);
          for (let i = 0; i < this.topicToCategory.length; i++) {
            this.topicToCategory[i] = {
              text: this.topicToCategory[i].category,
              value: this.topicToCategory[i].pk,
            };
          }
          console.log(this.topicToCategory);
        })
        .catch(function(error) {
          console.log(error);
        });
    },
    getAllStudentsInTopic() {
      // console.log(this.data);
      axios
        .get(
          `${API_URL}/students_in_topic/${this.data.course.id}/${
            this.data.topic.id
          }/`
        )
        .then(student => {
          // console.log(student);
          this.students = student.data;
          console.log(this.students);
        })
        .catch(function(error) {
          console.log(error);
        });
    },
    addStudentGrade() {
      // Check to see if the form is correct
      if (
        !this.newTopicToCategory.category ||
        !this.newTopicToCategory.student ||
        !this.newTopicToCategory.description ||
        !this.newTopicToCategory.weight
      ) {
        this.openToast();
        this.setToastInfo({
          type: 'error',
          title: 'Could not add Grade',
          message: 'Please add all fields',
          duration: 6000,
        });
      } else {

        const profile = JSON.parse(localStorage.getItem('profile'));
        // Create post object
        const gradeData = {
          token: profile.auth.profile.id_token,
          topic_to_category: this.newTopicToCategory.category,
          value: this.newTopicToCategory.weight,
          student: this.newTopicToCategory.student,
          name: this.newTopicToCategory.description,
        };



        // Post and create
        axios
          .post(`${API_URL}/grades/`, gradeData)
          .then(response => {})
          .catch(error => {
            console.log(error);
            this.openToast();
            this.setToastInfo({
              type: 'error',
              title: 'Could not add grade',
              message: 'Please try again',
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
          console.log(this.topicToCategory);

          const profile = JSON.parse(localStorage.getItem('profile'));

          // Delete the resource
          axios
            .delete(`${API_URL}/topic/category/${this.topicToCategory[n].pk}/?id_token=${profile.auth.profile.id_token}`)
            .then(function(response) {
              console.log(response);
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

<template>
  <div v-if="isOpen" class="topic-modal" @click.self="closeModal()">
    <div class="content">
      <h2 class="title">{{ pageTitle }} - {{ topicGrade }}% Complete</h2>
      <sui-icon @click="closeModal()" name="close icon" class="close-modal-button"/>
      <template v-if="!data.locked">
        <div class="tab-nav">
          <span
            class="link"
            @click="context = 'resources'"
            :style="{ color: context === 'resources' ? 'var(--color-green-40)' : 'var(--color-green-50)'}"
          >Resources</span>
          <span
            class="link"
            @click="context = 'quiz'"
            :style="{ color: context === 'quiz' ? 'var(--color-green-40)' : 'var(--color-green-50)'}"
          >Quizzes</span>
          <!-- Only show for professor -->
          <span
            v-if="role === 'professor'"
            class="link"
            @click="context = 'topic_settings'"
            :style="{ color: context === 'topic_settings' ? 'var(--color-green-40)' : 'var(--color-green-50)'}"
          >Topic Settings</span>
          <span
            v-if="role === 'professor'"
            class="link"
            @click="context = 'update_student_grades'"
            :style="{ color: context === 'update_student_grades' ? 'var(--color-green-40)' : 'var(--color-green-50)'}"
          >Update Student Grades</span>
          <span
            class="link"
            @click="context = 'studentgrades'"
            :style="{ color: context === 'studentgrades' ? 'var(--color-green-40)' : 'var(--color-green-50)'}"
          >View Grades</span>
        </div>
        <div class="main">
          <Resources
            v-if="context === 'resources'"
            :role="role"
            :data="data"
            :topicId="data.topic.id"
          />
          <Quiz v-if="context === 'quiz'" :topicId="data.topic.id"/>
          <TopicSettings
            v-if="context === 'topic_settings'"
            :role="role"
            :data="data"
            :topicId="data.topic.id"
          />
          <TopicStudentGrades
            v-if="context === 'update_student_grades'"
            :role="role"
            :data="data"
            :topicId="data.topic.id"
          />
          <!-- Switch to student grade component -->
          <TopicStudentGrade
            v-if="context === 'studentgrades'"
            :role="role"
            :data="data"
            :topicId="data.topic.id"
          />
        </div>
      </template>
      <div v-else>
        <h2>You haven't unlocked this topic yet</h2>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Quiz from '@/components/quiz/Quiz';
import Resources from '@/components/Resources';
import TopicSettings from '@/components/TopicSettings';
import TopicStudentGrade from '@/components/TopicStudentGrade';
import TopicStudentGrades from '@/components/TopicStudentGrades';
import { API_URL } from '@/constants';

export default {
  components: {
    Quiz,
    Resources,
    TopicSettings,
    TopicStudentGrade,
    TopicStudentGrades,
  },
  props: {
    role: {
      type: String,
      default: 'professor',
    },
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
      context: 'quiz',
      pageTitle: '',
      topicGrade: '',
    };
  },

  mounted() {},
  created() {},
  updated() {
    this.topicGrade = this.data.grade;
    this.pageTitle = this.data.topic.name;
  },

  methods: {
    closeModal(event) {
      this.$emit('onClose');
    },
    addResource() {
      if (!this.newResource.name || !this.newResource.link) {
        alert('Need to fill both fields');
      } else {
        if (this.newResource.link) {
          if (this.newResource.link.substring(0, 4) != 'www.') {
            var temp = this.newResource.link;
            this.newResource.link = 'www.' + temp;
          }
          if (this.newResource.link.substring(0, 8) != 'https://') {
            var temp = this.newResource.link;
            this.newResource.link = 'https://' + temp;
          }
        }
        this.resources.push({
          name: this.newResource.name,
          link: this.newResource.link,
        });

        const resourceData = {
          name: this.newResource.name,
          link: this.newResource.link,
          topic: this.data.topic.id,
        };

        axios
          .post(`${API_URL}/resources/`, resourceData)
          .then(function(response) {
            this.retrieveResources();
          })
          .catch(function(error) {});

        this.newResource.name = '';
        this.newResource.link = '';
        this.saveResources();
      }
    },

    removeResource(n) {
      console.log(this.resources[n].pk);
      axios
        .delete(`${API_URL}/resources/${this.resources[n].pk}`)
        .then(function(response) {
          //this.resources.splice(n, 1);
          //this.retrieveResources();
          //this.saveResources();
          console.log(response);
        })
        .catch(function(error) {
          console.log(error);
        });
    },
  },
};
</script>

<style scoped>
.tab-nav {
  padding-bottom: 8pt;
  margin-bottom: 8pt;
  border-bottom: var(--color-green-10) 0.75pt solid;
}
.tab-nav .link {
  font-weight: bold;
  font-size: 12pt;
  margin-right: 8pt;
  cursor: pointer;
}
.topic-modal {
  position: absolute;
  top: 0;
  left: 0;
  z-index: 1000000;
  width: 100%;
  height: 100%;
  border-radius: 6pt;
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
  min-width: 500pt;
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
.main {
  height: 375pt;
}
</style>

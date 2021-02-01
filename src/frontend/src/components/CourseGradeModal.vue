<template>
<!-- TODO: Name is sligly confusing. Maybe change it to CourseGradeInfo? -->
<!-- TODO: Modal currently opens in pull page context, try to use same context as 'TopicModal' -->
  <div v-if="isOpen" class="topic-modal" @click.self="closeModal()">
    <div class="content" style="margin-top: 8pt; overflow-y: scroll">
      <h2 class="title">{{ pageTitle }} Grading Info</h2>
      <sui-icon @click="closeModal()" name="close icon" class="close-modal-button"/>
      <!-- take out extraneous code later -->
      <template v-if="true">
        <div class="tab-nav">
          <span
            class="link"
            @click="context = 'overview'"
            :style="{ color: context === 'overview' ? 'var(--color-green-40)' : 'var(--color-green-50)'}"
          >Overview</span>
      
          <span
            class="link"
            @click="context = 'progress'"
            :style="{ color: context === 'progress' ? 'var(--color-green-40)' : 'var(--color-green-50)'}"
          >Progress</span>
          <!-- Only show for professor -->
          <span
            v-if="role === 'professor'"
            class="link"
            @click="context = 'edit_grading_scale'"
            :style="{ color: context === 'edit_grading_scale' ? 'var(--color-green-40)' : 'var(--color-green-50)'}"
          >Edit Grading Scale</span>
        </div>
        <!--
        <div class="main">
          <Resources
            v-if="context === 'resources'"
            :role="role"
            :data="data"
            :topicId="data.topic.id"
          />
          <TopicSettings
            v-if="context === 'topic_settings'"
            :role="role"
            :data="data"
            :topicId="data.topic.id"
          />
          <TopicAddGrade
            v-if="context === 'topic_add_grade'"
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
          <!-- Switch to student grade component
          <TopicStudentGrade
            v-if="context === 'studentgrades'"
            :role="role"
            :data="data"
            :topicId="data.topic.id"
          />
          <TopicTakeQuiz
            v-if="context === 'take_quiz'"
            :role="role"
            :data="data"
            :topicId="data.topic.id"
          />
        </div>
        -->
      </template>
      <div v-else>
        <h2>Unreachable</h2>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
//import CourseGradeInfo from '@/components/CourseGradeInfo';
//import CourseGradeProgress from '@/components/CourseGradeProgress';
//import CourseGradeEditScale from '@/components/CourseGradeEditScale';

import { API_URL } from '@/constants';

export default {
  components: {
    //CourseGradeInfo,
    //CourseGradeProgress,
    //CourseGradeEditScale,
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
      context: 'overview',
      pageTitle: '',
    };
  },

  mounted() {},
  created() {},
  updated() {
    this.pageTitle = this.data.subjectCode + this.data.courseCode;
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
        .delete(`${API_URL}/resources/${this.resources[n].pk}/`, { headers: { Authorization: `Bearer ${this.profile.id_token}` } })
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
  height: 100%;
}
</style>

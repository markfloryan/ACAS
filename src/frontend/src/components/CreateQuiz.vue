<template>
    <div>
        <div class="quizCreator" v-if="page < 2">
            <div class="title" style="padding:10px">
                <h3 v-if="page == 0">Create quizzes</h3>
                <h3 v-if="page == 1">Quiz Info</h3>
            </div> 
            <div class="content" v-if="page === 0">
                <h4>Select a Topic</h4>
                <sui-form-field>
                    <sui-dropdown
                    placeholder="Select topic"
                    :options="topics"
                    selection
                    search
                    v-model="topicPK"
                    />
                </sui-form-field>
                <h4 v-if="topicPK !== null">Select an Assignment</h4>
                <sui-form-field>
                    <sui-dropdown
                        placeholder="Select assignment"
                        v-if="topicPK !== null"
                        :options="assignments"
                        selection
                        search
                        v-model="assignmentPK"
                    />
                </sui-form-field>
            </div>
            <div class="content" v-if="page === 1">
                <sui-form-field>
                    <h4>Select and Open and Close Date for the Quiz</h4>
                    <h5>Open Date</h5>
                    <input v-model="openDate" placeholder="DatePicker">
                    <h5>Close Date</h5>
                    <input v-model="closeDate" placeholder="DatePicker">
                    <h4>Type of Quiz</h4>
                    <sui-dropdown
                        placeholder="Select type of quiz"
                        :options="quizTypes"
                        selection
                        search
                        v-model="quizPK"
                    />
                </sui-form-field>
            </div>
            <div class="buttons">
                <button
                    :class="disableBack ? 'btn btn-disabled' : 'btn btn-primary edit-btn'"
                    :disabled="disableBack ? true : false"
                    :style="disableBack ? '' : returnPrimaryButtonStyle"
                    data-toggle="tooltip"
                    data-placement="bottom"
                    title="Previous Step"
                    @click="prevPage()"
                >Back</button>
                <button
                    class="btn btn-primary edit-btn"
                    :style="returnPrimaryButtonStyle"
                    style="float: right;"
                    data-toggle="tooltip"
                    data-placement="bottom"
                    title="Next Step"
                    @click="nextPage()"
                >Next</button>
            </div>
        </div>
        <div v-if="page >= 2">
            <QuestionWriter :topicPK="topicPK" :assignmentPK="assignmentPK"></QuestionWriter>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { mapGetters, mapState, mapMutations } from 'vuex';
import { API_URL } from '@/constants';
import QuestionWriter from '@/components/QuestionWriter';

export default {
  components: { QuestionWriter },
  /*
  Defines the data used by the component
  */
  data(){
    return {
      file: '',
      page: 0,
      disableBack: true,
      disableNext: false,
      topics: [],
      topicPK: null,
      assignments: [],
      assignmentPK: null,
      openDate: null,
      closeDate: null,
      quizTypes: [],
      quizPK: null,
    };
  },
  mounted() {
    this.getTopics();
    this.quizTypes = [{text: 'Practice', value: 0}, {text: 'Graded', value: 1}];
  },
  watch: {
    topicPK: function (){
      this.getAssignments(this.topicPK);
    }
  },
  props: {
    courseId: {
      type: String,
      required: true,
    }
  },
  computed: {
    ...mapState('auth', ['profile']),
    ...mapGetters('settings', ['returnPrimaryButtonStyle']),
  },
  methods: {
    ...mapMutations('toast', ['openToast', 'setToastInfo']),
    nextPage() {
      if (!this.validate()) {
        this.openToast();
        this.setToastInfo({
          type: 'error',
          title: 'Error',
          message: 'Page not complete',
          duration: 10000,
        });
        return;
      }
      this.page += 1;
      if(this.page == 0) {
        this.disableBack = true;
      } else {
        this.disableBack = false;
      }

      if (this.page == 2) {
        this.openToast();
        this.setToastInfo({
          type: 'success',
          title: 'Created Quiz',
          message: 'Successfully created a quiz',
          duration: 10000,
        });
        //this would then call save or create quiz or whatever
      }
    },
    prevPage() {
      this.page -= 1;
      if(this.page == 0) {
        this.disableBack = true;
      } else {
        this.disableBack = false;
      }
    },
    validate() {
      if(this.page == 0) {
        return this.topicPK != null && this.assignmentPK != null;
      } else if (this.page == 1) {
        return this.openDate != null && this.closeDate != null && this.quizPK != null;
      } else {
        return true;
      }

    },
    getAssignments() {
      axios.get(`${API_URL}/assignments/?topicId=${this.topicPK}`, 
        { 
          headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: `Bearer ${this.profile.id_token}`
          }
        }).then((response)=> {
        let data = response.data.result;
        this.assignments = [];
        for(let i=0;i<data.length;i++){
          let assignment = data[i];
          this.assignments.push({
            text: assignment.name,
            value: assignment.pk
          });
        }
      }).catch(function(){

      });
    },
    getTopics() {
      axios.get(`${API_URL}/topics/?courseId=${this.courseId}`, 
        { 
          headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: `Bearer ${this.profile.id_token}`
          }
        }).then((response)=> {
        let data = response.data.result;
        for(let i=0;i<data.length;i++){
          let topic = data[i];
          this.topics.push({
            text: topic.name,
            value: topic.pk
          });
        }
      }).catch(function(){

      });
    },
    saveQuiz() {
      this.openToast();
      this.setToastInfo({
        type: 'error',
        title: 'Error',
        message: 'Not Implemented Yet',
        duration: 10000,
      });
    }
  } 
};
</script>


<style scoped>
.quizCreator {
    display: grid;
    grid-template-areas:
        'title'
        'content'
        'buttons';
    grid-template-columns: 1fr;
    grid-template-rows: 1fr 8fr 1fr;
}
.title {
    grid-area: title;
    padding-left: 10pt;
    padding-right: 10pt;
}
.buttons {
    grid-area: buttons;
    padding-left: 10pt;
    padding-right: 10pt;
}
.content {
    grid-area: content;
    padding-left: 10pt;
    padding-right: 10pt;
}
</style>

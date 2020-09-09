<template>
    <div class="container">
        <div class="large-12 medium-12 small-12 cell" style="padding:10px">
        <h3>Upload quizzes</h3>
        <h5>CSV schema (Note: if a quiz for the assignment already exists, it will be deleted and a new quiz will be created)</h5>
        <p>First line: # of multiple choice, # of free response, # of select all that apply, # of parsons problems</p>
        <p>Multiple choice question line 1: 0, answer_index</p>
        <p>Multiple choice question line 2: question, first_choice, second_choice, third_choice...</p>
        <h4>Quiz Assignment</h4>
        <sui-form-field>
          <sui-dropdown
            placeholder="Select assignment"
            :options="assignments"
            selection
            search
            v-model="assignmentPK"
          />
        </sui-form-field>
        <label>
            <input type="file" id="file2" ref="file2" v-on:change="handleQuizFileUpload()"/>
        </label>
        <button v-on:click="submitQuizFile()">Upload</button>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { mapGetters, mapState, mapMutations } from 'vuex';
import { API_URL } from '@/constants';
export default {
  /*
  Defines the data used by the component
  */
  data(){
    return {
      file: '',
      assignments: [],
      assignmentPK: null,
    };
  },
  mounted() {
    this.getAssignments();
  },
  props: {
    courseId: {
      type: String,
      required: true,
    }
  },
  computed: {
    ...mapState('auth', ['profile']),
  },
  methods: {
    ...mapMutations('toast', ['openToast', 'setToastInfo']),
    handleQuizFileUpload() {
      this.file2 = this.$refs.file2.files[0];
    },
    submitQuizFile(){
      let formData = new FormData();
      formData.append('csv', this.file2);

      let localID = this.profile.id_token;
      if(this.assignmentPK == null){
        this.openToast();
        this.setToastInfo({
          type: 'error',
          title: 'Error',
          message: 'Assignment not selected',
          duration: 10000,
        });
        return;
      }

      axios
        .post( `${API_URL}/assignmentQuizUpload/${this.assignmentPK}`,
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data',
              Authorization: `Bearer ${this.profile.id_token}`
            }
          }
        ).then((response)=> {
        //for (i=0; i<response.data.errors.length; i++) {
          if(response.data.ok) {
            this.openToast();
            this.setToastInfo({
              type: 'success',
              title: 'Successful Upload',
              message: 'Quiz successfully uploaded',
              duration: 5000,
            });
          }
          else {
            this.openToast();
            this.setToastInfo({
              type: 'error',
              title: 'Uploading Error',
              message: `${response.data.errors}`,
              duration: 10000,
            });
          }
          /*
          setTimeout(function(){ 
            openToast();
            this.setToastInfo({
              type: 'error',
              title: 'Uploading Error',
              message: `${response.data.errors[1]}`,
              duration: 6000,
          }); }, 6000);*/
        //}
        
        }).catch(function(){
          console.log('Quiz upload failure');
        });
    },
    getAssignments(){
      axios.get(`${API_URL}/assignments/?courseId=${this.courseId}`, 
        { 
          headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: `Bearer ${this.profile.id_token}`
          }
        }).then((response)=> {
        let data = response.data.result;
        for(let i=0;i<data.length;i++){
          let assignment = data[i];
          this.assignments.push({
            text: assignment.name,
            value: assignment.pk
          });
        }
        //console.log("Assignments: " + this.assignments[0].name);
      }).catch(function(){

      });
    }
  } 
};
</script>

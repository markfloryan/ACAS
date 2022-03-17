<template>
  <div>
    <h1 v-if="create">Create a new section:</h1>
    <h1 v-if="!create">Edit this section:</h1>
    <sui-form @submit.prevent>
      <sui-form-field>
        <label>Section name</label>
        <input v-model="sname" placeholder="Section name" type="text">
      </sui-form-field>
      <sui-form-field>
        <label>Section code</label>
        <input v-model="scode" placeholder="Section code" type="text">
      </sui-form-field>
      <div>
        <sui-form-field>
          <label>First Open Date and Time</label>
          <Datepicker v-model="sdate" type="datetime"></Datepicker>
        </sui-form-field>
        <sui-form-field>
          <label>Duration</label>
          <input v-model="sduration" placeholder="Duration" type="number">
        </sui-form-field>
        <sui-form-field>
          <label>Frequency</label>
          <sui-dropdown
            placeholder="Frequency"
            :options="frequency"
            selection
            search
            v-model="frequencyPK"
            />
        </sui-form-field>
      </div>
      <div style="text-align: center;">
        <button type="button" @click="closeModal()" style="margin: 8pt;"  class="btn btn-plain cancel-btn">Cancel</button>
        <button v-if="create" type="button" @click="createSection()" style="margin: 8pt;" class="btn btn-create create-btn">Create</button>
        <button v-if="!create" type="button" @click="updateSection()" style="margin: 8pt;" class="btn btn-create create-btn">Update</button>
      </div>
    </sui-form>
  </div>
</template>

<script>
import axios from 'axios';
import { mapGetters, mapState, mapMutations } from 'vuex';
import Datepicker from 'vue2-datepicker';
import 'vue2-datepicker/index.css';
import { API_URL } from '@/constants';

export default {
  name: 'EditSection',
  components: {
    Datepicker,
  },
  props: {
    prefill: {
      type: Object,
      required: false,
    },
    create: {
      type: Boolean,
      required: true,
    },
    course: {
      type: String,
      required: true,
    }
  },
  data() {
    return {
      sname: '',
      scode: '',
      sdate: null,
      sduration: 30,
      frequency: [],
      frequencyPK: null,
    };
  },
  mounted() {
    console.log('mounting edit');
    if(this.prefill != null) {
      this.sname = this.prefill.name;
      this.scode = this.prefill.section_code;
      this.sduration = this.prefill.open_duration;
      this.frequencyPK = this.prefill.frequency;
      this.sdate = new Date(this.prefill.next_open_date);
    }
    this.frequency = [{value: 0, text: 'Once'},
        {value: 1, text: 'Daily'},
        {value: 7, text: 'Weekly'},
        {value: 14, text: 'Biweekly'}];
  },
  created() {
    // console.log(this.data);
  },
  computed: {
    ...mapState('auth', ['profile']),
    ...mapGetters('settings', ['returnPrimaryButtonStyle']),
  },
  methods: {
    ...mapMutations('toast', ['openToast', 'setToastInfo']),
    closeModal() {
      this.$emit('onClose');
    },
    createSection() {
      let sectionData = {
        course: this.course,
        name: this.sname,
        section_code: this.scode,
        frequency: this.frequencyPK,
        next_open_date: this.sdate.toISOString(),
        open_duration: this.sduration,
      };

      axios
        .post(`${API_URL}/sections/`, sectionData, { headers: { Authorization: `Bearer ${this.profile.id_token}` } })
        .then(response => {
          if(response.status == 200) {
            this.openToast();
            this.setToastInfo({
              type: 'success',
              title: 'Successful Creation',
              message: 'Section successfully created',
              duration: 5000,
            });
            this.closeModal();
          }
        })
        .catch(error => {
          console.log(error);
        });
    },
    updateSection() {
      let sectionData = {
        course: this.course,
        name: this.sname,
        section_code: this.scode,
        frequency: this.frequencyPK,
        next_open_date: this.sdate.toISOString(),
        open_duration: this.sduration,
      };

      axios
        .put(`${API_URL}/sections/${this.prefill.pk}`, sectionData, { headers: { Authorization: `Bearer ${this.profile.id_token}` } })
        .then(response => {
          if(response.status == 200) {
            this.openToast();
            this.setToastInfo({
              type: 'success',
              title: 'Successful Update',
              message: 'Section successfully updated',
              duration: 5000,
            });
            this.closeModal();
          }
        })
        .catch(error => {
          console.log(error);
        });
    }
  }
};
</script>
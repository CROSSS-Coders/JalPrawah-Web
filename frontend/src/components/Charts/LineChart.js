import { Line, mixins } from "vue-chartjs";
// import globalOptionsMixin from "@/components/Charts/globalOptionsMixin";

export default {
  name: "line-chart",
  extends: Line,
  mixins: [mixins.reactiveProp],
  props: {
    extraOptions: {
      type: Object,
      default: () => ({})
    },
    chartData: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      ctx: null
    };
  },
  watch: {
    chartData() {
      this.renderChart(this.chartData, this.extraOptions);
    }
  },
  mounted() {
    this.$watch(
      "chartData",
      (newVal, oldVal) => {
        if (!oldVal) {
          this.renderChart(this.chartData, this.extraOptions);
        }
      },
      { immediate: true }
    );
  }
};

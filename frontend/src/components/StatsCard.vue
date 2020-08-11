<template>
  <card class="card-stats" :show-footer-line="true">
    <div class="row">
      <div class="col">
        <slot>
          <h5 class="card-title text-uppercase mb-0" v-if="title">{{ title }}</h5>
          <span class="font-weight-bold mb-0" :class="subTitleClasses" v-if="subTitle">
            {{
            subTitle
            }}
          </span>
        </slot>
      </div>

      <div class="col-auto p-1" v-if="$slots.icon || icon">
        <slot name="icon">
          <div
            class="icon icon-shape text-white rounded-circle shadow"
            :class="[`bg-${type}`, iconClasses]"
          >
            <i :class="icon"></i>
          </div>
        </slot>
      </div>
      <div class="col-auto p-1" v-if="$slots.emoji || emoji">
      <slot name="emoji">
        <span class="h1 text-xl" v-if="emoji">{{emoji}}</span>
      </slot>
    </div>
    </div>
    

    <p class="mt-1 mb-0 text-sm">
      <slot name="footer"></slot>
    </p>
  </card>
</template>
<script>
import Card from "./Card.vue";

export default {
  name: "stats-card",
  components: {
    Card
  },
  props: {
    type: {
      type: String,
      default: "primary"
    },
    icon: String,
    title: String,
    subTitle: [String, Number],
    iconClasses: [String, Array],
    subTitleClasses: [String, Array],
    emoji: String
  }
};
</script>
<style></style>

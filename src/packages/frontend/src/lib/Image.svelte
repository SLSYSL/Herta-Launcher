<!--
Copyright The Apache Software Foundation

Modified by LANREN on 2026/2/2 for add some features
-->
<script lang="ts">
    export let data: { [key: string]: any };
</script>
<img src="{data.attr.source}" alt="" class:disabled={String(data.attr.disabled??"")=="true"} style="
    margin: {data.attr.margin ?? 0};
    width: {data.attr.width ?? 'auto'};
    height: {data.attr.height ?? 'auto'};
    align-self: {data.attr.align ?? 'center'};
">
<style lang="scss">
    img{
        display: flex;
        max-width: 100%;
    }
</style>
{% macro generate_schema_name(custom_schema_name, node) -%}

    {% if node.name.startswith('stg_') %}
        STAGING

    {% elif node.name.startswith('int_') %}
        INTERMEDIATE

    {% elif node.name.startswith('dim_') %}
        MART

    {% elif node.name.startswith('fct_') %}
        MART

    {% elif custom_schema_name is not none %}
        {{ custom_schema_name | trim }}

    {% else %}
        {{ target.schema }}

    {% endif %}

{%- endmacro %}
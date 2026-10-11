# {{ title }}

Chronohex: `{{ chronohex }}`
Selection: `{{ selector }}`
Entries: **{{ entries | length }}**

{% for entry in entries %}
---

## {{ loop.index }}. {{ entry.display_heading }}

- **ID:** `{{ entry.id }}`
{% if entry.parent_id %}- **Parent:** `{{ entry.parent_id }}`
{% endif %}{% if entry.source_path %}- **Source:** `{{ entry.source_path }}`
{% endif %}- **Record:** `{{ entry.review_file }}:{{ entry.review_line }}`
{% if entry.word_count %}- **Words:** {{ entry.word_count }}
{% endif %}{% if entry.augment_model %}- **Model:** `{{ entry.augment_model }}`
{% endif %}{% if entry.liber963_part %}- **Part:** `{{ entry.liber963_part }}`
{% endif %}{% if entry.chapter_verb %}- **Chapter verb:** `{{ entry.chapter_verb }}`
{% endif %}{% if entry.ascendant_sign %}- **Ascendant:** `{{ entry.ascendant_sign }}`
{% endif %}{% if entry.blended_sign %}- **Blended sign:** `{{ entry.blended_sign }}`
{% endif %}{% if entry.invocation_n %}- **Invocation:** {{ entry.invocation_n }}
{% endif %}{% if entry.unity %}- **Unity:** {{ entry.unity }}
{% endif %}{% if entry.augment_error %}- **Error:** `{{ entry.augment_error }}`

{% endif %}
{# Preserve a Markdown block boundary after the optional metadata rows. #}

{% if entry.augment_error %}### Augment error

> [!warning]
> {{ entry.augment_error }}

{% endif %}{% if entry.augment_output %}### Model-generated text

{{ entry.augment_output | blockquote }}

{% endif %}{% if entry.translation %}### Translation

{{ entry.translation }}

{% if entry.system %}**System** — {{ entry.system }}{% endif %}{% if entry.mode %} · **Mode** — {{ entry.mode }}{% endif %}

{% if entry.key_names %}### Keys

{{ entry.key_names | list }}

{% endif %}{% endif %}### Original

{{ entry.text }}
{% if not loop.last %}

{% endif %}{% endfor %}

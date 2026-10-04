# Croppy: offline coffee-farm helper for smallholders

**Track:** Agriculture (Annex B), Small AI for Development Hackathon (Hack-Nation × World Bank, Oct 2026)
**Platform:** the household's existing Android smartphone (an offline web app, no install store needed), plus SMS, which reaches any basic phone. No extra hardware.
Note: AI Tools have been used to develop this application
## The decision chain (Annex B: "what is affecting her crop" and "what it is worth")
1. **Check:** choose Coffee or Beans and photograph a leaf. On-phone AI models identify coffee rust, leaf miner, Cercospora, Phoma or healthy, and bean angular leaf spot, bean rust or healthy. A model says **"Not a coffee/bean leaf"** for other plants, and **"Not sure, ask a person"** when unsure. Advice is spoken in Kiswahili or English, and weather context is added ("the last two weeks favour rust").
2. **Alerts:** transparent weather rules over the offline region pack flag rust risk, cold nights, dry spells, heat and the harvest season, and show soil notes (pH, nitrogen, organic matter).
3. **Sell:** a fair-price band for this month, the 6-month trend, and how far the buyer's offer is from fair. Records harvest and sales, stock left and its worth, and yield per hectare against the national average. **Croppy never says when to sell.**
4. **My farm:** the farm profile doubles as a **consent-based registry record** she can SMS to her co-op. This answers the brief's point that a missing farmer registry is often the binding constraint.
5. **Records:** leaf checks, harvests and sales, all on the phone, exportable as CSV, sent to the extension officer by SMS only when she chooses.

## What is AI and what is not (be upfront in the video)
| Part | Method | Why |
|---|---|---|
| Leaf diagnosis | **AI:** two MobileNetV3-Small classifiers (coffee, beans), each with an `other` reject class, uint8-quantised, about 1–2 MB each, on the phone | SMS, a spreadsheet or a search cannot tell rust from leaf miner in a photo |
| Photo quality gate | Rules (brightness, blur) | Stops the model guessing on bad photos |
| Alerts, soil notes | Rules, shown with their reasons | Transparent and checkable. A learned risk model needs labelled outbreak data we do not have |
| Fair price | Reference data (median and quartiles of recent prices) | Deliberately no forecasting: a confident wrong price prediction harms her livelihood |

## Rules check (Section 06)
- **Device she has:** the household smartphone, plus SMS to and from basic phones.
- **Offline core:** the model, region pack (about 5 KB), advice and records are all on the phone. A service worker caches the app.
- **Small model:** about 1–2 MB, side-loadable over Bluetooth or WhatsApp (*My farm → Load model files*).
- **Local language:** Kiswahili. For less-supported languages (Luganda, Lumasaba): pre-recorded clips by co-op members, and contributing recordings to Mozilla Common Voice.
- **Human in the loop:** fixed answers only, no chemical doses, a "not sure" threshold tuned for ≥95% accuracy on answers given, every SMS reviewed and sent by her, and no sell or wait advice.

## Run it
1. **Leaf models:** run `training/train_croppy_colab.ipynb` (T4 GPU, about 60–75 minutes). Unzip `croppy_coffee_model.zip` into `app/model/` and `croppy_beans_model.zip` into `app/model_beans/`.
2. **Region pack:** run `training/build_region_pack_colab.ipynb`. Set the coordinates, upload the WFP price CSV, and enter the coffee farm-gate prices and FAOSTAT yields. Copy `pack.json` to `app/region/pack.json`. The bundled pack is **synthetic demo data** and the app shows a banner until you replace it.
3. **Voice (optional):** run `training/make_audio.py` in Colab to make MMS-TTS clips in `app/audio/`.
4. **Host:** push `app/` to GitHub Pages (HTTPS). Open it once on the phone, *Add to Home screen*, then demo in airplane mode. For a local test, use `cd app && python3 -m http.server 8000`.

## Data
**Built with (Annex B.2):**
| Dataset | Use |
|---|---|
| BRACOL | Coffee model training (5 classes) |
| iBean (Makerere, TFDS `beans`) | Bean model training (3 classes, Ugandan field photos), plus negatives for the coffee model |
| PlantVillage (TFDS) + PlantDoc | `other` reject class only: studio + field photos of non-coffee/non-bean plants. Soybean excluded from the bean model's negatives |
| RoCoLe + own photos | Field test only |

**Annex B.2 datasets not used yet (roadmap):** CHIRPS (finer rainfall for alerts), iSDAsoil at 30 m (finer soil), LSMS-ISA ("farms like yours" yield benchmark), Sentinel-2 / Landsat / Digital Earth Africa (canopy change), Cassava Leaf Disease (not Noor's crop).
**Region pack:** NASA POWER (weather), ISRIC SoilGrids or iSDAsoil (soil), WFP food prices via HDX (maize, beans), the national coffee board or co-op (coffee farm-gate price), FAOSTAT (national yield), FAO GIEWS crop calendar (harvest months).
**Problem evidence:** FAOSTAT yield trend, GSMA Mobile Gender Gap, and the Annex B note that the extension officer visits about twice a year.

**What our data does not cover** (scored):
- The coffee images come from Brazil in controlled conditions. iBean is Ugandan field photos, but only 3 bean conditions. The `other` class can't cover every plant, weed or object. Field light, varieties and backgrounds differ, and we report the field-test drop.
- There are no berry diseases, nutrient deficiencies, drought stress, mixed infections or early symptoms. These go to "Not sure", or the healthy-leaf advice points to other causes.
- NASA POWER is a coarse grid (about 50 km) and lags a few days. It can't see the microclimate of one slope.
- SoilGrids is modelled at 250 m, not a soil test. Soil notes say "ask the officer", never a dose.
- WFP covers staples, not coffee. Coffee prices depend on a manual farm-gate source, and grade and quality premiums are not captured.
- No plot-level yield data exists: yield per hectare comes only from what she records.

## Privacy
Everything is stored on the phone. GPS is opt-in. The co-op registry record is sent only with an explicit consent tick, by an SMS she reviews. *Delete all records* clears the phone. There are no accounts and no cloud.

## Video outline (2–5 minutes)
1. **Problem statement:** "Because of Croppy, Noor will spot coffee leaf rust the week it appears and know whether a buyer's offer is fair before she sells, instead of waiting months for the extension officer and accepting whatever the middleman names; we know because extension visits reach her sub-county about twice a year and [FAOSTAT yield / price evidence]."
2. **Why AI:** the image model is the AI. Everything else is deliberately simple and transparent. Then cover the guardrails.
3. **Demo in airplane mode:** leaf → rust + weather context → listen → SMS officer → Alerts → Sell (an offer 13% below fair) → My farm registry SMS. Then show a blurry photo producing "Not sure".
4. **Your take:** what localising AI means to you.

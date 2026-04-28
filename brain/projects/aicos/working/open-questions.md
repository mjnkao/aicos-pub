# Câu Hỏi Còn Mở Của AICOS

Trạng thái: câu hỏi còn mở.

1. Khi nào nên activate A2-Serve như một runtime/service lane thật?
2. Khi nào nên canonicalize sâu hơn các file như `architecture.md`,
   `promotion-policy.md`, `capsule-contract.md`, `branch-contract.md`?
3. Khi nào `aicos option choose` cần thêm policy sâu hơn như actor registry,
   reason taxonomy, hoặc review signature?
4. Chính sách cost/rate-limit nào nên áp dụng cho `aicos sync brain` full
   import và background embedding refresh khi chạy trên team/server runtime?
5. MCP stdio wrapper riêng của AICOS nên làm ở phase nào?
6. Full JSON Schema validation nên thêm ngay hay chờ packet shape ổn định?
7. Legacy backup nào nên migrate trước, và tiêu chí review là gì?
8. Khi nào nên tách `RUL-26088` thành permanent class-specific rule files?
9. Khi nào cần tạo actor registry/review signature cho manager decision thay vì
   chỉ ghi `--actor` và markdown approval packet?
10. Khi nào candidate branch ideas đủ chín để tạo branch reality chính thức
    trong `brain/projects/aicos/branches/`?
11. Khi nào nên mở rộng `./aicos context start` ngoài MVP hiện tại
    (`A2-Core-C`, `projects/aicos`)?
12. Khi nào startup output nên có one-line summary cho từng task packet để chọn
    packet nhanh hơn?
13. Khi nào nên xử lý nhất quán PATH/command để dùng được `aicos ...` thay vì
    chỉ chắc chắn với `./aicos ...`?
14. Khi nào nên tách shared operating policies để A1 tái sử dụng mà không kéo
    theo A2-Core taxonomy?
15. Khi nào nên thêm provider-backed hoặc serving-backed registries mỏng cho
    task packets, handoffs, queues, candidate decisions, hoặc sync ledger mà
    vẫn giữ markdown truth là semantic core?
16. Khi nào nên audit backup handoff cũ trong
    `backup/handoff-provenance-20260418/` để trích thêm nội dung còn giá trị vào
    self-brain mới?
17. Nên thiết kế information architecture markdown-first của AICOS theo mô hình
    nào để brain vừa human-readable, vừa agent-readable, nhưng không phình thành
    các file quá dài và khó bảo trì?
18. Nên định nghĩa multi-resolution reading cho project docs như thế nào để
    CEO/CTO/architect/worker có thể đọc ở mức phù hợp mà vẫn bám cùng một truth?
19. Nên chuẩn hóa các structural primitives nào ở cấp AICOS (summary, detail,
    index, decision, working-state, handoff, evidence, context-ladder, task
    packet, ...) để các project giữ được consistency mà không bị ép cùng một
    template cứng?
20. Nên cho phép project-specific information architecture profile ở mức nào để
    các dự án rất khác nhau vẫn tổ chức knowledge tốt mà không drift quá mạnh?
21. Tiêu chí nào nên dùng để tách một tài liệu thành nhiều module, tạo thêm
    summary/index/view, hoặc giữ nó là một doc duy nhất?
22. Làm sao phân định rõ hơn giữa truth gốc và các audience-specific views để
    tránh việc nhiều bản summary/detail dần trở thành nhiều nguồn sự thật?
23. Nên reuse GBrain ở mức nào cho AICOS search/query: chỉ học pattern,
    wrap engine/search primitives, hay nhận cả skill/recipe/integration
    surfaces? Ranh giới nào giữ được AICOS authority model mà vẫn tránh tự code
    lại phần retrieval tốt đã có?
24. Nên chuẩn hóa compatibility matrix cho MCP clients ở mức nào để tránh mỗi
    client lại kéo thêm một tactical auth/transport path riêng?
25. Trong 4 gap lớn giữa AICOS và GBrain về search/query
    (eval+verify, direct-get/mode arbitration, chunking, relation-aware
    retrieval), nên đóng gap nào trước để tăng retrieval quality nhiều nhất mà
    vẫn không kéo AICOS lệch sang page-schema/link-graph architecture?
26. AICOS có nên chuyển rõ sang mô hình "semantic/control-plane layer on top
    of a GBrain-derived substrate" không? Nếu có, boundary kỹ thuật nào phải
    giữ bất biến để tránh AICOS drift thành page-centric knowledge product thay
    vì multi-agent project control-plane?
27. "Company knowledge for AI agents" nên được hiểu ở mức nào trong tương lai:
    chỉ những knowledge surfaces cần cho vận hành project/coordination, hay
    dần mở rộng sang broader company memory? Ranh giới nào giúp AICOS không
    phình thành universal knowledge tool quá sớm?
28. Nên chuẩn hóa actor-role model của AICOS tới mức nào để vừa giữ rõ
    `A1`/`A2` cho internal AICOS maintenance, vừa không áp taxonomy này lên
    các project khác vốn có thể cần functional roles và service roles rất
    khác nhau?

## Closed Question: blocker-001 option choice

Closed by manager decision at `2026-04-18T04:15:56+00:00`.

- Blocker: `blocker-001`
- Selected option: `option-a`
- Selected branch: `blocker-001-option-a`

## Closed Question: sample project first slice and import

Closed during `sample-project` promotion/import work.

- Old name: Crypto Trading
- Active project id: `projects/sample-project`
- Result: first slice/import-truth questions are resolved for AICOS onboarding;
  import kit material is now provenance/reference.
